from typing import Optional, Callable, Any

from data_plumber import Pipeline, Stage

from data_plumber_http.output import Output
from data_plumber_http.settings import Responses
from .conditional_key import _ConditionalKey


class OneOf(_ConditionalKey):
    """
    A `OneOf` paired with a `Mapping` can be passed to an `Object`
    constructor (`properties` argument) as a form of conditional
    request body validation. It is processed such that only one of
    the properties in the associated `Mapping` are included in the
    output.

    Keyword arguments:
    name -- name identifier for this key
    exclusive -- if `True`, require that exactly one match is made
                 (default `True`)
    default -- either static value or callable taking input kwargs; used
               as default if property is missing in request
               (default `None`)
    required -- if `True`, this property is marked as required
                (default `False`)
    validation_only -- skip exporting this property to the resulting
                       data and only perform validation
                       (default `False`)
    """

    def __init__(
        self,
        name: str,
        exclusive: bool = True,
        default: Optional[Callable[..., Any] | Any] = None,
        required: bool = False,
        validation_only: bool = False
    ) -> None:
        self.exclusive = exclusive
        self.name = name
        self.default = default
        self.required = required
        self.validation_only = validation_only

    @staticmethod
    def _arg_exists_hard(loc, origins):
        def status(json, EXPORT_options, EXPORT_matches, **kwargs):
            if EXPORT_matches:
                return Responses().GOOD.status
            for k in json:
                if k in EXPORT_options \
                        and EXPORT_options[k].last_status != Responses().GOOD.status:
                    return EXPORT_options[k].last_status
            return Responses().MISSING_REQUIRED_ONEOF.status

        return Stage(
            status=status,
            message=lambda EXPORT_options, EXPORT_matches, **kwargs:
                Responses().GOOD.msg if EXPORT_matches
                else Responses().MISSING_REQUIRED_ONEOF.msg.format(
                    options=", ".join(map(lambda x: f"'{x}'", origins)),
                    loc=loc,
                    details=", ".join(
                        map(
                            lambda x: f"'{x}': \"{EXPORT_options[x].last_message or '<missing>'}\"",
                            EXPORT_options.keys()
                        )
                    )
                )
        )

    @staticmethod
    def _arg_exists_soft():
        def status(json, EXPORT_options, EXPORT_matches, **kwargs):
            if EXPORT_matches:
                return Responses().GOOD.status
            for k in json:
                if k in EXPORT_options \
                        and EXPORT_options[k].last_status != Responses().GOOD.status:
                    return EXPORT_options[k].last_status
            return Responses().MISSING_OPTIONAL.status

        def message(json, EXPORT_options, EXPORT_matches, **kwargs):
            if EXPORT_matches:
                return Responses().GOOD.msg
            for k in json:
                if k in EXPORT_options:
                    return Responses().BAD_VALUE_IN_ONEOF.msg.format(
                        child=EXPORT_options[k].last_message
                    )
            return Responses().MISSING_OPTIONAL.msg

        return Stage(
            status=status,
            message=message
        )

    @staticmethod
    def _exclusive_match(name, loc, origins):
        return Stage(
            requires={f"{name}[exists]": Responses().GOOD.status},
            status=lambda EXPORT_matches, **kwargs:
                Responses().GOOD.status if len(EXPORT_matches) == 1
                else Responses().MULTIPLE_ONEOF.status,
            message=lambda EXPORT_matches, **kwargs:
                Responses().GOOD.msg if len(EXPORT_matches) == 1
                else Responses().MULTIPLE_ONEOF.msg.format(
                    property="property" if len(origins) == 1 else "properties",
                    options=", ".join(map(lambda x: f"'{x}'", origins)),
                    loc=loc,
                    matches=", ".join(map(lambda x: f"'{x}'", EXPORT_matches))
                )
        )

    @staticmethod
    def _output():
        return Stage(
            primer=lambda EXPORT_options, EXPORT_matches, **kwargs:
                EXPORT_options[EXPORT_matches[0]].data.kwargs if EXPORT_matches
                else {},
            action=lambda out, primer, **kwargs:
                [
                    out.update({"kwargs": {}})
                    if "kwargs" not in out
                    else None,
                    out.kwargs.update(primer)
                ],
            status=lambda **kwargs: Responses().GOOD.status,
            message=lambda **kwargs: Responses().GOOD.msg
        )

    def assemble(self, value, loc):
        p = Pipeline(
            exit_on_status=lambda status: status >= 400,
            initialize_output=Output
        )
        _loc = loc or "."

        # run options
        p.append(
            f"{self.name}[options]",
            **{f"{self.name}[options]": self._run_options(value, _loc)}
        )

        # evaluate options
        # validate existence
        if self.required and self.default is None:
            p.append(
                f"{self.name}[exists]",
                **{
                    f"{self.name}[exists]":
                        self._arg_exists_hard(_loc, self.get_origins(value))
                }
            )
        else:
            p.append(
                f"{self.name}[exists]",
                **{
                    f"{self.name}[exists]":
                        self._arg_exists_soft()
                }
            )

        # validate exclusiveness
        if self.exclusive:
            p.append(
                f"{self.name}[exclusive]",
                **{
                    f"{self.name}[exclusive]":
                        self._exclusive_match(
                            self.name, _loc, self.get_origins(value)
                        )
                }
            )

        # stop here if requested
        if self.validation_only:
            return p

        # set default
        if self.default is not None:
            p.append(
                f"{self.name}[default]",
                **{f"{self.name}[default]": self._set_default(self)}
            )

        # output
        p.append(
            f"{self.name}[output]",
            **{f"{self.name}[output]": self._output()}
        )

        return p

from sfn_messages.core.enum_mixin import EnumMixin


class CertificateIssue(EnumMixin):
    SERPRO = 1
    CERTISIGN = 2
    SERASA = 4
    AC_CAIXA = 5
    AC_VALIDA = 6
    AC_SOLUTI = 7

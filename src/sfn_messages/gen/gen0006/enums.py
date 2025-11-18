from sfn_messages.core.enums import EnumMixin


class MessageCode(EnumMixin):
    GEN0006 = 'GEN0006'
    GEN0006R1 = 'GEN0006R1'


class CertificateIssue(EnumMixin):
    SERPRO = 1
    CERTISIGN = 2
    SERASA = 4
    AC_CAIXA = 5
    AC_VALIDA = 6
    AC_SOLUTI = 7

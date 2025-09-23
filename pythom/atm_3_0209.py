import time


class Account:
    def __init__(self, passWord: int, agency: int, number: int, balance: float, keyPix: str):
        self.passWord = passWord
        self.agency = agency
        self.number = number
        self.balance = balance
        self.youPix = keyPix
(""")
    def startScreen:
    (""")
(""")
    "primeiramente loga conta,agencia e senha que ja foi passada pelo sistema"
            "caso usuario erra mostra que ele apenas erro não fala oque ele errou"
                "ao iniciar mostra seu nome agencia,conta e saldo, podendo ser"
                " negativo ou positivo"
                    "sempre ao final de cada operação mostra/notifica oq foi feito"
   
    def chargePassWord:
        "usuario pdoer altera sua senha, padrao"
            "logo que ele fazer logoff sera nessesario fazer uso de sua nova senha"


    def currentKeyPix:
        "na primeira vez mostra sem chave pix cadastrada"
            "logo apos ele podendo cadastra uma chave pix valida como numero de cell ou email"
                "sempre ao final de cada operação mostra/notifica oq foi feito"
   
   def limit:
        "vino ja com um limit padrao, ele podendo ajusta esse limite o quanto quiser"
            "sempre ao final de cada operação mostra/notifica oq foi feito"
   
   def seedPix:
        "verificar se o clietente tem saldo/limit"
            "pode fazer o uso de limite para fazer o pix sendo onde ex:"
            " se ele tem saldo de 400 e quer fazer um pix de 1000, ele "
            "fazer o uso do limite dele sendo que seu limite foi "
            "ajustado para 2000, ele fazendo o pix e ficando com 1600"
             "sempre ao final de cada operação mostra/notifica oq foi feito"
   
    def statement:
        "mostra as movimentações da conta oque foi mandado ou recebido"



(""")






(""")
========================================
|                                      |
|          WELCOME TO PYATM            |
|                                      |
========================================
|          [1] Check Balance           |
|          [2] Deposit                 |
|          [3] Withdraw                |
|          [4] Transfer via PIX        |
|          [5] Change Password         |
|          [6] Set / Change PIX Key    |
|          [7] Adjust Limit            |
|          [8] Exit                    |
========================================
      [C] CANCEL  [L] CLEAR  [E] ENTER |
")    
(""")
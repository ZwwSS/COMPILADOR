import ply.lex as lex
import ply.yacc as yacc

#PARTE LEXICA
#Definición de Palabras reservadas
reservadas = {
    'ari', #si
    'chaykama', #mientras
    'imprimiy' , #imprimir
    'chaymanta', #y
    'manam', #no
    'utaq' #o 
}
# Definición de tokens
tokens = [
    'SEMICOLON', #punto y coma
    'LLUQI_LLAVE', #Llave izquierda
    'PAÑA_LLAVE', #llave derecha
    'CHAYKAQLLA', #igual
    'CHAYKAQLLAQ', #igual que 
    'YUYAQ', #mayor que
    'PISI', #menor que 
    'YUYAQCHAY', #mayor o igual  
    'YUYAQPISI', #menor o igual
    'HUK_NIRAQ', #diferente que 
    'ISKAY_PUNTO', #dos puntos
    'YUPAY', #numero
    'YAPAY', #suma
    'QICHUY', #resta
    'MIRACHIY', #multiplicacion 
    'RAKINAKUY', #division
    'LLUQI_PAREN', #parentesis d
    'PAÑA_PAREN', #parentesis i
] + list(reservadas.values())

# Expresiones regulares para los tokens
t_YAPAY = r'\+'
t_QICHUY = r'-'
t_MIRACHIY = r'\*'
t_RAKINAKUY = r'/'
t_PAÑA_PAREN = r'\('
t_LLUQI_PAREN = r'\)'
t_SEMICOLON = r';'
t_LLUQI_LLAVE = r'{'
t_PAÑA_LLAVE = r'}'
t_CHAYKAQLLA = '='
t_CHAYKAQLLAQ = '=='
t_YUYAQ = '>'
t_PISI = '<'
t_YUYAQCHAYL = '>='
t_YUYAQPISI = '<='
t_HUK_NIRAQ = '!='
t_ISKAY_PUNTO = ':'

# Detectar e Ignorar espacios y saltos de línea
t_ignore = ' \t\n'
#def t_nuevalinea (t):
#    r'\n+'
#    t.lexer.lineno == len(t.value)


def t_NUMERO(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_COMENTARIO(t):
    r'\#.*'
    pass

#deteccion del identificador para retornarlo
def t_ID(t):
    r'[a-zA-Z][a-zA0-9]*'
    #transforma el token en minusculas
    t.type = reservadas.get(t.value.lower(),'ID')
    return t

#Deteccion de enteros
def t_ENTERO(t):
    r'\d*'
# Manejo de errores
def t_error(t):
    print(f"Carácter inesperado: '{t.value[0]}'")
    t.lexer.skip(1)

# Construcción del analizador léxico
lexer = lex.lex()

# Reglas de la gramática
def p_expresion(p):
    '''expresion : expresion SUMA termino
                 | expresion RESTA termino
                 | termino'''
    if len(p) == 2:
        p[0] = p[1]
    elif len(p) == 4:
        if p[2] == '+':
            p[0] = p[1] + p[3]
        elif p[2] == '-':
            p[0] = p[1] - p[3]

def p_termino(p):
    '''termino : termino MULTI factor
               | termino DIVISION factor
               | factor'''
    if len(p) == 2:
        p[0] = p[1]
    elif len(p) == 4:
        if p[2] == '*':
            p[0] = p[1] * p[3]
        elif p[2] == '/':
            p[0] = p[1] / p[3]

def p_factor(p):
    '''factor : NUMERO
              | PARENTESIS_IZQ expresion PARENTESIS_DER'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = p[2]


# Manejo de errores de sintaxis
def p_error(p):
    print("Error de sintaxis en '%s'" % p.value if p else "Error de sintaxis")

# Construcción del analizador sintáctico
parser = yacc.yacc()


# Ejemplo de uso
if __name__ == '_main_':
    data = input("Ingresa una expresión matemática: ")
    result = parser.parse(data)
    print(f"Resultado: {result}")



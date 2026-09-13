def on_change_custo(e):
    value = e.control.value
    
    # Mantém apenas os dígitos numéricos
    digits = "".join([c for c in value if c.isdigit()])
    
    if not digits:
        e.control.value = ""
        e.control.update()
        return

    # Converte os dígitos acumulados em um número inteiro e divide por 100 para criar os centavos
    integer_value = int(digits)
    float_value = integer_value / 100
    
    # Formata no padrão brasileiro: pontos nos milhares e vírgula nos decimais (ex: 12.345,67)
    # :邻,.2f cria o formato americano (12,345.67), depois trocamos os caracteres
    new_val = f"{float_value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    
    # Atualiza o campo apenas se o valor mudou (evita loops infinitos)
    if value != new_val:
        e.control.value = new_val
        e.control.update()

texto = "Pontuacao Professor: {'Grande dificuldade': [{'primarias': ['vermelho', 'azul', 'amarelo'], 'secundarias': ['roxo', 'verde', 'laranja']}], 'Leve dificuldade': [{'primarias': [], 'secundarias': []}]}"

# Remover caracteres indesejados
texto_limpo = texto.replace("{", "").replace("}", "").replace("[", "").replace("]", "").replace("'", "")

print(texto_limpo)

from surf_simulation.prancha import Prancha
from surf_simulation.condicoes import Condicoes
import condicoes

def escolher_prancha(condicoes):
    pranchas = ["5'8", "5'11", "6'2"]

    # Converter condicoes.tamanho_onda para float
    tamanho_onda_num = float(condicoes.tamanho_onda)

    # Usar tamanho_onda_num nas comparações
    if tamanho_onda_num < 3:
       return pranchas[0]  # Ondas pequenas: prancha menor
    elif 3 <= tamanho_onda_num < 6:  # Ondas médias: entre 3 e 5 pés
     print("Prancha escolhida: intermediária")
     return pranchas[1]
    elif 7 <= tamanho_onda_num < 10:  # Ondas grandes: entre 5 e 6 pés
     print("Prancha escolhida: grande")
     return pranchas[2]
    else:  # Ondas muito grandes: acima de 6 pés
     print("Procure abrigo! Ondas muito grandes são perigosas.")
    return None

if __name__ == "__main__":
    tamanho_onda = input("Digite o tamanho das ondas (em pés): ")
    condicoes_atuais = condicoes.Condicoes(tamanho_onda)
    prancha_escolhida = escolher_prancha(condicoes_atuais)

    print(f"\nCondições: Ondas de {condicoes_atuais.tamanho_onda} pés")
    print(f"Prancha escolhida: {prancha_escolhida}")
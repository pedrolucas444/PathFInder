import unittest
from main import ler_labirinto, busca_a_estrela, distancia_manhattan

class TesteBuscaEstrela(unittest.TestCase):
    def test_ler_labirinto_valido(self):
        labirinto = ["S 0 1", "0 0 E"]
        grade, inicio, fim = ler_labirinto(labirinto)
        self.assertEqual(inicio, (0, 0))
        self.assertEqual(fim, (1, 2))
    
    def test_sem_caminho(self):
        labirinto = ["S 1", "1 E"]
        grade, inicio, fim = ler_labirinto(labirinto)
        caminho, _, _ = busca_a_estrela(grade, inicio, fim)
        self.assertIsNone(caminho)

    def test_distancia_manhattan(self):
        a = (0, 0)
        b = (3, 4)
        self.assertEqual(distancia_manhattan(a, b), 7)

if __name__ == "__main__":
    unittest.main()
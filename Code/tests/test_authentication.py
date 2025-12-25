
import sys
import os

# Ajoute le répertoire parent au path pour pouvoir importer app
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.models.UserDAO import UserDAO

def test_authentication():
    """
    Teste l'authentification pour 3 utilisateurs:
    1. Romain (admin)
    2. Tristan (communication)
    3. Abou (commercial)
    
    Le mot de passe pour tous est '12345' (défini dans initdb.py)
    """
    
    print("=== TEST D'AUTHENTIFICATION ===\n")
    
    # Création d'une instance du DAO
    dao = UserDAO()
    
    # Liste des utilisateurs à tester
    test_users = [
        {"username": "Romain", "password": "12345", "expected_role": "admin"},
        {"username": "Tristan", "password": "12345", "expected_role": "communication"},
        {"username": "Abou", "password": "12345", "expected_role": "commercial"}
    ]
    
    # Compteurs de résultats
    tests_passed = 0
    tests_failed = 0
    
    # Test pour chaque utilisateur
    for user_test in test_users:
        username = user_test["username"]
        password = user_test["password"]
        expected_role = user_test["expected_role"]
        
        print(f"Test de {username}...")
        
        # Vérification 1: L'utilisateur existe-t-il ?
        user = dao.findByUsername(username)
        if user is None:
            print(f"   ÉCHEC: Utilisateur '{username}' non trouvé dans la base\n")
            tests_failed += 1
            continue
        
        # Vérification 2: Le mot de passe est-il correct ?
        if not dao.verifyUser(username, password):
            print(f"  ❌ ÉCHEC: Mot de passe incorrect pour '{username}'\n")
            tests_failed += 1
            continue
        
        # Vérification 3: Le rôle est-il correct ?
        if user.role != expected_role:
            print(f"  ❌ ÉCHEC: Rôle incorrect pour '{username}'")
            print(f"     Attendu: {expected_role}, Obtenu: {user.role}\n")
            tests_failed += 1
            continue
        
        # Si on arrive ici, tous les tests sont passés
        print(f"  ✅ SUCCÈS: {username} authentifié correctement (rôle: {user.role})\n")
        tests_passed += 1
    
    # Affichage du résumé
    print("=== RÉSUMÉ DES TESTS ===")
    print(f"Tests réussis: {tests_passed}/3")
    print(f"Tests échoués: {tests_failed}/3")
    
    if tests_passed == 3:
        print("\n TOUS LES TESTS SONT PASSÉS AVEC TOUT LE RESPECT !")
        return True
    else:
        print("\n⚠️  CERTAINS TESTS ONT ÉCHOUÉ LES MECS ILS ONT PASSSSSSS")
        return False

def test_wrong_password():
    """
    Vérifie que l'authentification échoue avec un mauvais mot de passe
    """
    print("\n=== MAUVAIS MOT DE PASSE ===\n")
    
    dao = UserDAO()
    
    # Tentative avec un mauvais mot de passe
    if dao.verifyUser("Romain", "wrongpassword"):
        print(" ÉCHEC: Le système a accepté un mauvais mot de passe !")
        return False
    else:
        print(" SUCCÈS: Le système a bien rejeté le mauvais mot de passe")
        return True

if __name__ == "__main__":
    # Lance les tests
    auth_ok = test_authentication()
    bonus_ok = test_wrong_password()
    
    # Code de sortie (0 = succès, 1 = échec)
    sys.exit(0 if (auth_ok and bonus_ok) else 1)
"""
EXPLICATION DU TEST:
-------------------
On vérifie que :
1. Un utilisateur 'admin' peut accéder aux pages admin (devices, logs, tools)
2. Un utilisateur 'communication' peut accéder à devices et timetable mais PAS aux logs
3. Un utilisateur 'commercial' peut accéder à devices et timetable mais PAS aux logs

Comment ça marche ?
- On simule une connexion pour chaque utilisateur
- On essaie d'accéder à différentes pages
- On vérifie le code HTTP retourné :
  * 200 = OK, accès autorisé
  * 403 = Forbidden, accès refusé (c'est normal pour certains rôles)
  * 302 = Redirect (souvent vers la page de login si pas connecté)
"""

import sys
import os

# Ajoute le répertoire racine au path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app
from app.models.UserDAO import UserDAO

def test_admin_access():
    """
    Teste que l'utilisateur ADMIN a accès à toutes les pages
    
    Pages testées:
    - /devices/<orga> : Doit être accessible (200)
    - /logs/<orga> : Doit être accessible (200)
    - /dashboard/<orga> : Doit être accessible (200)
    """
    print("\n=== TEST ACCÈS ADMIN ===")
    
    with app.test_client() as client:
        # Connexion en tant qu'admin (Romain)
        response = client.post('/login', data={
            'username': 'Romain',
            'password': '12345'
        }, follow_redirects=True)
        
        # Vérifie que la connexion a réussi
        if response.status_code != 200:
            print("❌ ÉCHEC: Impossible de se connecter en tant qu'admin")
            return False
        
        print("✅ Connexion admin réussie")
        
        # Nom d'une organisation de test (d'après initdb.py)
        orga = "Harman_Kardon"
        
        # Test 1: Accès à /devices
        response = client.get(f'/devices/{orga}')
        if response.status_code == 200:
            print(f"  ✅ Admin peut accéder à /devices/{orga}")
        else:
            print(f"  ❌ Admin ne peut PAS accéder à /devices/{orga} (code: {response.status_code})")
            return False
        
        # Test 2: Accès à /logs (réservé aux admins)
        response = client.get(f'/logs/{orga}')
        if response.status_code == 200:
            print(f"  ✅ Admin peut accéder à /logs/{orga}")
        else:
            print(f"  ❌ Admin ne peut PAS accéder à /logs/{orga} (code: {response.status_code})")
            return False
        
        # Test 3: Accès au dashboard
        response = client.get(f'/dashboard/{orga}')
        if response.status_code == 200:
            print(f"  ✅ Admin peut accéder à /dashboard/{orga}")
        else:
            print(f"  ❌ Admin ne peut PAS accéder à /dashboard/{orga} (code: {response.status_code})")
            return False
        
        print("✅ TOUS LES TESTS ADMIN PASSÉS\n")
        return True


def test_communication_access():
    """
    Teste que l'utilisateur COMMUNICATION a un accès limité
    
    Pages testées:
    - /devices/<orga> : Doit être accessible (200)
    - /dashboard/<orga> : Doit être accessible (200)
    - /logs/<orga> : NE doit PAS être accessible (403)
    """
    print("\n=== TEST ACCÈS COMMUNICATION ===")
    
    with app.test_client() as client:
        # Connexion en tant que communication (Tristan)
        response = client.post('/login', data={
            'username': 'Tristan',
            'password': '12345'
        }, follow_redirects=True)
        
        if response.status_code != 200:
            print("❌ ÉCHEC: Impossible de se connecter en tant que communication")
            return False
        
        print("✅ Connexion communication réussie")
        
        orga = "Harman_Kardon"
        
        # Test 1: Accès à /devices (devrait marcher)
        response = client.get(f'/devices/{orga}')
        if response.status_code == 200:
            print(f"  ✅ Communication peut accéder à /devices/{orga}")
        else:
            print(f"  ❌ Communication ne peut PAS accéder à /devices/{orga} (code: {response.status_code})")
            return False
        
        # Test 2: Accès au dashboard (devrait marcher)
        response = client.get(f'/dashboard/{orga}')
        if response.status_code == 200:
            print(f"  ✅ Communication peut accéder à /dashboard/{orga}")
        else:
            print(f"  ❌ Communication ne peut PAS accéder à /dashboard/{orga} (code: {response.status_code})")
            return False
        
        # Test 3: Accès à /logs (NE DEVRAIT PAS marcher - réservé admin)
        response = client.get(f'/logs/{orga}')
        if response.status_code == 403:
            print(f"  ✅ Communication ne peut PAS accéder à /logs/{orga} (comme attendu)")
        else:
            print(f"  ❌ PROBLÈME: Communication peut accéder à /logs/{orga} (code: {response.status_code})")
            print(f"     Attendu: 403 (Forbidden)")
            return False
        
        print("✅ TOUS LES TESTS COMMUNICATION PASSÉS\n")
        return True


def test_commercial_access():
    """
    Teste que l'utilisateur COMMERCIAL a un accès limité
    
    Pages testées:
    - /devices/<orga> : Doit être accessible (200)
    - /dashboard/<orga> : Doit être accessible (200)
    - /logs/<orga> : NE doit PAS être accessible (403)
    """
    print("\n=== TEST ACCÈS COMMERCIAL ===")
    
    with app.test_client() as client:
        # Connexion en tant que commercial (Abou)
        response = client.post('/login', data={
            'username': 'Abou',
            'password': '12345'
        }, follow_redirects=True)
        
        if response.status_code != 200:
            print("❌ ÉCHEC: Impossible de se connecter en tant que commercial")
            return False
        
        print("✅ Connexion commercial réussie")
        
        orga = "Harman_Kardon"
        
        # Test 1: Accès à /devices (devrait marcher)
        response = client.get(f'/devices/{orga}')
        if response.status_code == 200:
            print(f"  ✅ Commercial peut accéder à /devices/{orga}")
        else:
            print(f"  ❌ Commercial ne peut PAS accéder à /devices/{orga} (code: {response.status_code})")
            return False
        
        # Test 2: Accès au dashboard (devrait marcher)
        response = client.get(f'/dashboard/{orga}')
        if response.status_code == 200:
            print(f"  ✅ Commercial peut accéder à /dashboard/{orga}")
        else:
            print(f"  ❌ Commercial ne peut PAS accéder à /dashboard/{orga} (code: {response.status_code})")
            return False
        
        # Test 3: Accès à /logs (NE DEVRAIT PAS marcher - réservé admin)
        response = client.get(f'/logs/{orga}')
        if response.status_code == 403:
            print(f"  ✅ Commercial ne peut PAS accéder à /logs/{orga} (comme attendu)")
        else:
            print(f"  ❌ PROBLÈME: Commercial peut accéder à /logs/{orga} (code: {response.status_code})")
            print(f"     Attendu: 403 (Forbidden)")
            return False
        
        print("✅ TOUS LES TESTS COMMERCIAL PASSÉS\n")
        return True


def test_no_authentication():
    """
    Teste qu'un utilisateur NON connecté ne peut accéder à aucune page protégée
    
    Toutes les pages devraient rediriger vers /login (code 302)
    """
    print("\n=== TEST SANS AUTHENTIFICATION ===")
    
    with app.test_client() as client:
        orga = "Harman_Kardon"
        
        # Test 1: Tentative d'accès à /devices sans être connecté
        response = client.get(f'/devices/{orga}')
        if response.status_code == 302:  # 302 = Redirect vers login
            print(f"  ✅ Accès à /devices/{orga} redirige bien vers login")
        else:
            print(f"  ❌ PROBLÈME: /devices/{orga} accessible sans connexion (code: {response.status_code})")
            return False
        
        # Test 2: Tentative d'accès au dashboard sans être connecté
        response = client.get(f'/dashboard/{orga}')
        if response.status_code == 302:
            print(f"  ✅ Accès à /dashboard/{orga} redirige bien vers login")
        else:
            print(f"  ❌ PROBLÈME: /dashboard/{orga} accessible sans connexion (code: {response.status_code})")
            return False
        
        # Test 3: Tentative d'accès aux logs sans être connecté
        response = client.get(f'/logs/{orga}')
        if response.status_code == 302:
            print(f"  ✅ Accès à /logs/{orga} redirige bien vers login")
        else:
            print(f"  ❌ PROBLÈME: /logs/{orga} accessible sans connexion (code: {response.status_code})")
            return False
        
        print("✅ TOUS LES TESTS SANS AUTH PASSÉS\n")
        return True


if __name__ == "__main__":
    print("╔════════════════════════════════════════════╗")
    print("║   TEST D'ACCÈS AUX PAGES SELON LES RÔLES   ║")
    print("╚════════════════════════════════════════════╝")
    
    # Lance tous les tests
    admin_ok = test_admin_access()
    comm_ok = test_communication_access()
    commercial_ok = test_commercial_access()
    no_auth_ok = test_no_authentication()
    
    # Résumé final
    print("\n" + "="*50)
    print("RÉSUMÉ FINAL")
    print("="*50)
    print(f"Admin:          {'✅ PASSÉ' if admin_ok else '❌ ÉCHOUÉ'}")
    print(f"Communication:  {'✅ PASSÉ' if comm_ok else '❌ ÉCHOUÉ'}")
    print(f"Commercial:     {'✅ PASSÉ' if commercial_ok else '❌ ÉCHOUÉ'}")
    print(f"Sans auth:      {'✅ PASSÉ' if no_auth_ok else '❌ ÉCHOUÉ'}")
    print("="*50)
    
    # Code de sortie
    all_ok = admin_ok and comm_ok and commercial_ok and no_auth_ok
    
    if all_ok:
        print("\n TOUS LES TESTS SONT PASSÉS AVEC TOUT LE RESPECT!")
    else:
        print("\n CERTAINS TESTS ONT ÉCHOUÉ DONC LES MECS ILSS ONT PASSSSS")
    
    sys.exit(0 if all_ok else 1)
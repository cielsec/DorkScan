#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════════╗
║                    🔍 DORK SCANNER PRO v4.0                       ║
║              Usando DuckDuckGo (mais confiável)                  ║
╚══════════════════════════════════════════════════════════════════╝
"""

import requests
import time
import sys
import re
from urllib.parse import urlparse, quote_plus
from colorama import Fore, Style, init
from datetime import datetime

init(autoreset=True)

class DorkScanner:
    def __init__(self):
        self.valid_results = []
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
        })
        
    def banner(self):
        print(f"""{Fore.CYAN}{Style.BRIGHT}
    ██████╗  ██████╗ ██████╗ ██╗  ██╗    ███████╗ ██████╗ █████╗ ███╗   ██╗
    ██╔══██╗██╔═══██╗██╔══██╗██║ ██╔╝    ██╔════╝██╔════╝██╔══██╗████╗  ██║
    ██║  ██║██║   ██║██████╔╝█████╔╝     ███████╗██║     ███████║██╔██╗ ██║
    ██║  ██║██║   ██║██╔══██╗██╔═██╗     ╚════██║██║     ██╔══██║██║╚██╗██║
    ██████╔╝╚██████╔╝██║  ██║██║  ██╗    ███████║╚██████╗██║  ██║██║ ╚████║
    ╚═════╝  ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝    ╚══════╝ ╚═════╝╚═╝  ╚═╝╚═╝  ╚═══╝
{Fore.YELLOW}                    Dork Scanner Pro v1.0 by ciel - DuckDuckGo{Style.RESET_ALL}\n""")

    def log(self, msg, tipo="info"):
        ts = datetime.now().strftime("%H:%M:%S")
        icons = {'info': '*', 'ok': '+', 'warn': '!', 'err': '-', 'scan': '~', 'found': '→'}
        colors = {'info': Fore.BLUE, 'ok': Fore.GREEN, 'warn': Fore.YELLOW, 
                 'err': Fore.RED, 'scan': Fore.MAGENTA, 'found': Fore.CYAN}
        ic = colors.get(tipo, Fore.BLUE)
        print(f"{Style.DIM}[{ts}]{Style.RESET_ALL} {ic}[{icons[tipo]}]{Style.RESET_ALL} {msg}")

    def validate(self, url):
        """Valida se URL é acessível"""
        try:
            r = self.session.head(url, timeout=8, allow_redirects=True)
            if r.status_code in [200, 301, 302, 307, 308, 403, 401, 405, 500]:
                return True, r.status_code
            r = self.session.get(url, timeout=8, allow_redirects=True)
            return r.status_code in [200, 301, 302, 307, 308, 403, 401, 405, 500], r.status_code
        except Exception as e:
            return False, None

    def search_duckduckgo(self, dork, max_results=20):
        """
        Busca usando DuckDuckGo HTML - mais confiável que Google
        """
        self.log(f"Buscando: {Fore.CYAN}{dork}{Style.RESET_ALL}", "scan")
        urls = []
        
        try:
            # DuckDuckGo
            query = quote_plus(dork)
            url = f"https://html.duckduckgo.com/html/?q={query}"
            
            response = self.session.get(url, timeout=15)
            
            if response.status_code != 200:
                self.log(f"Erro HTTP {response.status_code}", "err")
                return urls
            
            
            
            pattern = r'<a[^>]+class="[^"]*result__a[^"]*"[^>]+href="([^"]+)"'
            matches = re.findall(pattern, response.text)
            
            
            if not matches:
                pattern = r'href="(https?://[^"]+)"'
                matches = re.findall(pattern, response.text)
            
            for link in matches:
               
                clean_url = link.split('&')[0].split('?')[0] if '&' in link or '?' in link else link
                
               
                if 'duckduckgo.com' in link or 'r.search.yahoo.com' in link:
                    
                    if 'uddg=' in link:
                        import urllib.parse
                        clean_url = urllib.parse.unquote(link.split('uddg=')[1].split('&')[0])
                    elif 'u=' in link:
                        clean_url = link.split('u=')[1].split('&')[0]
                    else:
                        continue
                
                
                if clean_url.startswith('http') and not any(x in clean_url.lower() for x in [
                    'duckduckgo.com', 'google.com', 'youtube.com', 'blogger.com',
                    'wordpress.com', 'wikipedia.org', 'facebook.com', 'twitter.com',
                    'instagram.com', 'linkedin.com', 'javascript:', 'mailto:'
                ]):
                    if clean_url not in urls:
                        urls.append(clean_url)
                        self.log(f"Encontrado: {Fore.CYAN}{clean_url}{Style.RESET_ALL}", "found")
                        
                        if len(urls) >= max_results:
                            break
            
            return urls
            
        except Exception as e:
            self.log(f"Erro na busca: {str(e)}", "err")
            return []

    def search_bing(self, dork, max_results=20):
        """
        Método alternativo usando Bing se DuckDuckGo falhar
        """
        self.log(f"Tentando Bing como alternativa...", "scan")
        urls = []
        
        try:
            query = quote_plus(dork)
            url = f"https://www.bing.com/search?q={query}&count={max_results}"
            
            response = self.session.get(url, timeout=15)
            
            
            pattern = r'<a[^>]+href="(https?://[^"]+)"[^>]*h="[^"]*"'
            matches = re.findall(pattern, response.text)
            
            for link in matches:
                if link.startswith('http') and not any(x in link.lower() for x in [
                    'bing.com', 'microsoft.com', 'google.com', 'youtube.com',
                    'facebook.com', 'twitter.com', 'javascript:', 'mailto:'
                ]):
                    if link not in urls:
                        urls.append(link)
                        self.log(f"Encontrado: {Fore.CYAN}{link}{Style.RESET_ALL}", "found")
                        
                        if len(urls) >= max_results:
                            break
            
            return urls
            
        except Exception as e:
            self.log(f"Erro no Bing: {str(e)}", "err")
            return []

    def scan(self, dork, validate=True, num=10):
        """Executa scan completo"""
        urls = self.search_duckduckgo(dork, num)
        
        
        if not urls:
            urls = self.search_bing(dork, num)
        
        if not urls:
            self.log("Nenhum resultado encontrado", "warn")
            return []
        
        self.log(f"{Fore.YELLOW}{len(urls)}{Style.RESET_ALL} resultados brutos", "ok")
        
        if not validate:
            return [(u, "N/A") for u in urls]
        
        self.log("Validando URLs (removendo falsos positivos)...", "scan")
        validos = []
        
        for url in urls:
            ok, status = self.validate(url)
            if ok:
                validos.append((url, status))
                self.log(f"[{Fore.GREEN}{status}{Style.RESET_ALL}] {url}", "ok")
            else:
                st = str(status) if status else "OFF"
                self.log(f"[{Fore.RED}{st}{Style.RESET_ALL}] {url}", "err")
            time.sleep(0.5)
        
        return validos

    def interactive(self):
        """Modo interativo"""
        self.banner()
        print(f"{Fore.YELLOW}Exemplos de Dorks:{Style.RESET_ALL}")
        print("  1. filetype:env DB_PASSWORD")
        print("  2. inurl:admin.php intitle:login")
        print("  3. intitle:index.of config.json")
        print("  4. ext:sql MySQL dump")
        print("  5. site:gov filetype:pdf\n")
        
        dorks = []
        while True:
            d = input(f"{Fore.CYAN}[?]{Style.RESET_ALL} Dork (ou 'scan'/'sair'): ").strip()
            if d.lower() == 'sair':
                sys.exit()
            elif d.lower() == 'scan':
                if not dorks:
                    self.log("Adicione pelo menos uma dork!", "warn")
                    continue
                break
            elif d:
                dorks.append(d)
                self.log(f"Adicionada: {d}", "ok")
        
        val = input(f"{Fore.CYAN}[?]{Style.RESET_ALL} Validar URLs? (S/n): ").strip().lower() != 'n'
        try:
            n = int(input(f"{Fore.CYAN}[?]{Style.RESET_ALL} Resultados por dork (padrão 10): ") or 10)
        except:
            n = 10
        
        print(f"\n{Fore.MAGENTA}{'='*50}{Style.RESET_ALL}")
        self.log(f"Iniciando scan de {Fore.YELLOW}{len(dorks)}{Style.RESET_ALL} dork(s)...", "info")
        print(f"{Fore.MAGENTA}{'='*50}{Style.RESET_ALL}\n")
        
        for i, dork in enumerate(dorks, 1):
            print(f"\n{Fore.CYAN}[{i}/{len(dorks)}]{Style.RESET_ALL} Processando...")
            r = self.scan(dork, val, n)
            if r:
                self.valid_results.append((dork, r))
                self.log(f"Concluído: {Fore.GREEN}{len(r)}{Style.RESET_ALL} URLs válidas", "ok")
            else:
                self.log("Concluído: Nenhum resultado válido", "warn")
            
            if i < len(dorks):
                time.sleep(3)
        
        self.summary()
        self.save()

    def summary(self):
        """Mostra resumo"""
        total = sum(len(r) for _, r in self.valid_results)
        print(f"\n{Fore.GREEN}{Style.BRIGHT}╔{'═'*48}╗")
        print(f"║{'RESUMO FINAL':^48}║")
        print(f"╠{'═'*48}╣")
        print(f"║ Dorks processadas: {len(self.valid_results):<29} ║")
        print(f"║ URLs válidas: {Fore.CYAN}{total}{Fore.GREEN}{' '*33}║")
        print(f"╚{'═'*48}╝{Style.RESET_ALL}")
        
        if self.valid_results:
            print(f"\n{Fore.CYAN}Detalhes:{Style.RESET_ALL}")
            for dork, res in self.valid_results:
                print(f"  {Fore.GREEN}•{Style.RESET_ALL} {dork}: {Fore.YELLOW}{len(res)}{Style.RESET_ALL} URLs")

    def save(self, fn="resultados_dork.txt"):
        """Salva resultados"""
        if not self.valid_results:
            self.log("Nenhum resultado para salvar", "warn")
            return
        
        try:
            with open(fn, 'w', encoding='utf-8') as f:
                f.write(f"DORK SCANNER PRO v4.0\n")
                f.write(f"Data: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"{'='*60}\n\n")
                
                for dork, res in self.valid_results:
                    f.write(f"[+] DORK: {dork}\n")
                    f.write("-" * 60 + "\n")
                    for url, status in res:
                        f.write(f"  [{status}] {url}\n")
                    f.write("\n")
            
            self.log(f"Resultados salvos em: {Fore.GREEN}{fn}{Style.RESET_ALL}", "ok")
        except Exception as e:
            self.log(f"Erro ao salvar: {e}", "err")

if __name__ == "__main__":
    try:
        DorkScanner().interactive()
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}[!] Scan interrompido pelo usuário{Style.RESET_ALL}")
        sys.exit(0)
    except Exception as e:
        print(f"\n{Fore.RED}[!] Erro: {e}{Style.RESET_ALL}")
        sys.exit(1)

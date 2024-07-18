import requests
from colorama import Fore, Style, init
import time
import argparse

init(autoreset=True)

banner_text = """
{green}
       .-''-.                                                .---.
     .' .-.  )                                               |   .--.  _..._       .
    / .'  / /                                                |   |__|.'     '.   .'|
   (_/   / /        .-''` ''-.       .-''` ''-.              |   .--.   .-.   ..'  |
        / /       .'          '.   .'          '.            |   |  |  '   '  <    |
       / /       /              ` /              `           |   .--.  |   |  ||   | ____
      . '       '                '                '          |   |  |  |   |  ||   | \ .'
     / /    _.-'|         .-.    |         .-.    |          |   |  |  |   |  ||   |/  .
   .' '  _.'.-''.        |   |   .        |   |   .          |   |__|  |   |  ||    /\  \\
  /  /.-'_.'     .       '._.'  / .       '._.'  /           '---'  |  |   |  ||   |  \  \\
 /    _.'         '._         .'   '._         .'                   |  |   |  |'    \  \  \\
( _.-'               '-....-'`        '-....-'`                     '--'   '--'------'  '---'

🌊 version 1.0.1 created by X-3nCrypt & ChatGPT4.0 with ❤️ 🌊
{reset}
""".format(green=Fore.GREEN, reset=Style.RESET_ALL)

def print_banner():
    print(banner_text)

def format_elapsed_time(seconds):
    if seconds < 60:
        return f"{seconds:.2f} seconds"
    elif seconds < 3600:
        minutes = seconds // 60
        seconds = seconds % 60
        return f"{minutes:.0f} minutes {seconds:.0f} seconds"
    else:
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        seconds = seconds % 60
        return f"{hours:.0f} hours {minutes:.0f} minutes {seconds:.0f} seconds"

def check_urls_from_file(file_path, output_file=None):
    total_urls = 0
    status_200 = 0
    status_301 = 0
    status_403 = 0
    status_404 = 0
    status_500 = 0
    other_status = 0
    start_time = time.time()
    successful_urls = []

    try:
        with open(file_path, 'r') as file:
            urls = file.readlines()
        urls = [url.strip() for url in urls if url.strip()]
        total_urls = len(urls)
    except Exception as e:
        print(f"Error reading file: {e}")
        return

    for url in urls:
        try:
            response = requests.head(url, timeout=5)
            status_code = response.status_code
            if status_code == 200:
                status_color = Fore.LIGHTGREEN_EX
                status_200 += 1
                successful_urls.append(url)
            elif status_code == 301:
                status_color = Fore.MAGENTA
                status_301 += 1
            elif status_code == 403:
                status_color = Fore.YELLOW
                status_403 += 1
            elif status_code == 404:
                status_color = Fore.RED
                status_404 += 1
            elif status_code == 500:
                status_color = Fore.RED
                status_500 += 1
            else:
                status_color = Fore.CYAN
                other_status += 1

            print(f"{Fore.WHITE}{url} {Fore.LIGHTRED_EX}: {status_color}{status_code}{Style.RESET_ALL}")
        except requests.ConnectionError:
            print(f"{Fore.RED}{url} {Fore.LIGHTRED_EX}: {Fore.RED}Failed to connect{Style.RESET_ALL}")
        except requests.Timeout:
            print(f"{Fore.RED}{url} {Fore.LIGHTRED_EX}: {Fore.RED}Timeout occurred{Style.RESET_ALL}")
        except requests.RequestException as e:
            print(f"{Fore.RED}{url} {Fore.LIGHTRED_EX}: {Fore.RED}Error occurred: {e}{Style.RESET_ALL}")

    end_time = time.time()
    elapsed_time = end_time - start_time
    formatted_time = format_elapsed_time(elapsed_time)

    print("\n{yellow}Total Scan{reset} : {blue}{total_urls}{reset} | {yellow}Time{reset} : {blue}{formatted_time}{reset} | {yellow}200 URL{reset} : {blue}{status_200}{reset} | {yellow}301 URL{reset} : {blue}{status_301}{reset} | {yellow}403 URL{reset} : {blue}{status_403}{reset} | {yellow}404 URL{reset} : {blue}{status_404}{reset} | {yellow}500 URL{reset} : {blue}{status_500}{reset} | {yellow}Other Status{reset} : {blue}{other_status}{reset}".format(
        yellow=Fore.YELLOW,
        blue=Fore.CYAN,
        reset=Style.RESET_ALL,
        total_urls=total_urls,
        formatted_time=formatted_time,
        status_200=status_200,
        status_301=status_301,
        status_403=status_403,
        status_404=status_404,
        status_500=status_500,
        other_status=other_status
    ))

    if output_file:
        try:
            with open(output_file, 'w') as file:
                for url in successful_urls:
                    file.write(url + '\n')
            print(f"\n{Fore.GREEN}Successfully saved 200 URLs to {output_file}{Style.RESET_ALL}")
        except Exception as e:
            print(f"\n{Fore.RED}Failed to save 200 URLs to {output_file}: {e}{Style.RESET_ALL}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="URL status checker")
    parser.add_argument('url_file', help="File containing list of URLs to check")
    parser.add_argument('-o', '--output', help="Output file to save 200 status URLs")
    args = parser.parse_args()

    print_banner()

    check_urls_from_file(args.url_file, args.output)

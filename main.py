import sys
from apps.registry import registry


def main():
    if sys.argv[1] == "list":
        registry.download_publications_list().execute()
    if sys.argv[1] == "info":
        registry.download_publications_info().execute()
    if sys.argv[1] == "pdf":
        registry.download_pdfs().execute()


if __name__ == "__main__":
    main()

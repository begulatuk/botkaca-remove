FROM beguganjang/botkaca:latest

COPY bot bot
CMD ["python3", "-m", "bot"]

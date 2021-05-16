FROM beguganjang/botkaca:latest

COPY bot bot
COPY start.sh .
CMD ["bash","start.sh"]

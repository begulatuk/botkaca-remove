FROM beguganjang/botkaca:latest

pip3 install -m -q lk21
COPY bot bot
COPY start.sh .
CMD ["bash","start.sh"]

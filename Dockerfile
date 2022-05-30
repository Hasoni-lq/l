FROM Hasoni-lq/l:slim-buster

#clonning repo 
RUN git clone https://github.com/Hasoni-lq/l.git /root/hsshh
#working directory 
WORKDIR /root/hsshh

# Install requirements
RUN pip3 install --no-cache-dir -r requirements.txt

ENV PATH="/home/hsshh/bin:$PATH"

CMD ["python3","-m","hsshh"]

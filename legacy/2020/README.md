# BBBot
## Um bot para votar no Big Brother Brasil 20
Desenvolvido para motivos de estudo, sem nenhuma intensão de prejuditar o programa, a emissora ou qualquer participante em epecífico

## Como utilizar:
Arquivo [creadentials.txt](https://github.com/IohanSardinha/BBBot/blob/master/credentials.txt) é onde ficam as informações de login, voto e url da votação

* Bibliotecas necessarias:
```
  -tkinter
  -selenium
  -Pillow
  -numpy
  -cv2
  -keras
  -tensorflow
  -tqdm
```

* Usando o modelo de previsão já criado
 
 Usando a interface grafica:
 
```
python bbbot.py
```

Usando o código em si:


```
python vote_bot.py
```






* Criando seu prório modelo de previsão
Primeiro é necessario obter as imagens para treinar o modelo, as imagens serão salvas na pasta _/objects_:

```
python get_images.py
```

Agora é preciso dividir as imagens obtidas de acordo com as possíveis categorias, colocando-as em pastas com os nomes das categorias no diretorio _/train_

Assim as imagens de frutas por exemplo ficariam em _/train/fruta_

Para criar as pastas necessárias pode-se usar o script auxiliar:

```
python create_folders.py
```

Para facilitar a classificação das imagens pode-se utilazar o [groupimg.py](https://github.com/IohanSardinha/BBBot/blob/master/groupimg.py). Script obtido em https://github.com/victorqribeiro/groupImg

```
python groupimg.py -f objects/ -k 60 -m
```

Com todas as imagens organizadar, basta apenas treinar o modelo:

```
python train_model.py
```

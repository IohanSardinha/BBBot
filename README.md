# BBBot
## Um bot para votar no Big Brother Brasil 21
Desenvolvido para motivos de estudo, sem nenhuma intensão de prejuditar o programa, a emissora ou qualquer participante em epecífico

## Como utilizar:
### Bibliotecas não built-in necessárias:
    - pynput (pip install pynput)

### Como executar:
```
> python repeater.py
```
O programa vai guardar o movimento do mouse e teclado até o usuário pressionar *Esc*, então repetirá o movimento guardado, até a tecla *Esc* ser pressionada novamente

### Funcionalidades adicionais:
    * Shift - Para de guardar até pressionar tab de novo
    * Control esquerdo - Irá parar a execução dos movimentos, até o píxel da posição do mouse quando ter a mesma cor de quando pressionado o shift
    * Esc(1) - Para de guardar e executa os movimentos
    * Esc(2) - Finaliza o programa, se estiver executando os movimentos
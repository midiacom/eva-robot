# Softare do robô EVA - Versão estendida da VPL 

Projeto de instalação dos módulos do Robô Conversacional EVA desenvolvido na CICESE no México. O objetivo deste repositório é armazenar o software do robô EVA com algumas melhorias propostas como parte do Estudo Orientado I.

## Detalhes da minha instalação
* É preciso criar a pasta temp no diretório da aplicação.
* Essa pasta está excluída no arquivo .gitignore pois ela contém os áudios das falas geradas pelo IBM Watson (lixo).

## Hardware
- Raspberry Pi 3B+ o 4B+
- Matrix Voice
- Servomotores Dynamixel AX-12A

## Instalação do Nodejs

- NodeJs 14.16.0
```bash
curl https://raw.githubusercontent.com/creationix/nvm/master/install.sh | bash
```
```bash
source ~/.profile
```
```bash
nvm install v14.16.0
```
```bash
nvm use v14.16.0
```
- Registrar a placa [Matrix Voice](https://matrix-io.github.io/matrix-documentation/matrix-voice/resources/microphone/) como microfone (Dispositivo de entrada)

```bash
curl https://apt.matrix.one/doc/apt-key.gpg | sudo apt-key add -
echo "deb https://apt.matrix.one/raspbian $(lsb_release -sc) main" | sudo tee /etc/apt/sources.list.d/matrixlabs.list
sudo apt-get update
sudo apt-get upgrade
```

```bash
sudo reboot
```

```bash
sudo apt install matrixio-kernel-modules
```

```bash
sudo reboot
```

### Dependências da Aplicação
### Rodar o comando seguinte dentro da pasta do EVA
```bash
npm install
```

### Copiar os arquivos para o dir do EVA:

"credencial.json" ... contêm a chave do Google Cloud

".env" .. contêm as credenciais do watson. achei estranho mas o arquivo deve
se chamar ".env". isso torna o arquivo invisivel no Linux

** Como dito anteriormente, é preciso criar uma pasta chamada "temp" no diretótio EVA.
Nele é que são criados os audios das falas geradas pelo o tts do IBM-Watson.

<!--
### Librerías
 - Requerida para compilar la dependencia "speaker".
```bash
sudo apt-get install libasound2-dev
```
-->


### Animações dos Leds da Matrix Voice

 - Pacotes necessários para compilar as animações dos leds da Matrix Voice.
```bash
sudo apt-get install matrixio-creator-init libmatrixio-creator-hal libmatrixio-creator-hal-dev
```
 - Para compilar as animações da Matrix Voice
```bash
g++ -o app app.cpp -std=c++11 -lmatrix_creator_hal
```

## Configuração

Arquivo necessário para o uso dos serviços text-to-speech do Watson:

- .env

Este arquivo deve conter os seguintes parâmetros:

```bash
TEXT_TO_SPEECH_APIKEY=api-key
TEXT_TO_SPEECH_URL=https://stream.watsonplatform.net/text-to-speech/api
```

<!-- Arquivo necessário para o uso dos serviços do Google:

- [Archivo JSON que contiene la clave de la cuenta de servicio de Google](https://cloud.google.com/docs/authentication/getting-started)
- Opcionalmente el archivo '.env' para la configuración de los servicios de Watson podrá contener el siguiente parámetro si se desea utlizar un proyecto de Dialogflow de Google por defecto:
```bash
DIALOGFLOW_PROJECT_ID=google-dialogflow-proyect-name
``` -->

Arquivo que inicia a aplicação de controle do robô EVA

- ini.sh

### O arquivo contêm o seguinte código:

 ```bash
 #!/bin/bash
echo Eva
sudo amixer cset numid=1 100% #volumen de la vocina
export GOOGLE_APPLICATION_CREDENTIALS="credencial.json" #importar las credenciales de google
npm run dev #Iniciar la aplicación
 ```

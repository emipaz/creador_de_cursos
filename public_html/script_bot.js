let conversationHistory = [];
const api = "http://localhost:5002/api"
document.addEventListener('DOMContentLoaded', function() {
        const contenidoHTML = `
            <div id="chatbot-circle">💬</div>
            <div id="chatbot-container">
                <div id="chatbot-main">
                    <h1>${title}</h1>
                    <iframe id="chatbotFrame" src="" width="100%" height="400" frameborder="0">
                        <head>
                            <meta charset="UTF-8">
                            <meta name="viewport" content="width=device-width, initial-scale=1.0">                            
                        </head>
                    </iframe>
                    <textarea id="inputQuestion" rows="4" placeholder="Escribe tu pregunta aquí..."></textarea>
                    <button id="sendButton">Enviar</button>
                    <p id="instructionText">Presiona Enter para enviar. Shift + Enter para un salto de línea.</p>
                </div>
            </div>
        `;
    
        const nuevoDiv = document.createElement('div');
        nuevoDiv.id = 'chatbot';
        nuevoDiv.innerHTML = contenidoHTML;
        document.body.appendChild(nuevoDiv);
    
        // Agregar el evento de clic al círculo de chatbot
        document.getElementById('chatbot-circle').addEventListener('click', toggleChatbot);
        // Agregar el evento de clic al botón de enviar
        document.getElementById('sendButton').addEventListener('click', sendQuestion);

        // Agregar el evento de teclado para el envío y salto de línea
        document.getElementById('inputQuestion').addEventListener('keydown', function(event) {
            if (event.key === 'Enter') {
                if (event.shiftKey) {
                    // Salto de línea
                    event.preventDefault();
                    const cursorPos = this.selectionStart;
                    const textBeforeCursor = this.value.substring(0, cursorPos);
                    const textAfterCursor = this.value.substring(cursorPos);
                    this.value = textBeforeCursor + '\n' + textAfterCursor;
                    this.selectionStart = cursorPos + 1;
                    this.selectionEnd = cursorPos + 1;
                } else {
                    // Enviar mensaje
                    event.preventDefault();
                    sendQuestion();
                }
            }
        });
    
        // carga los estilos de la ventana del chatbot
        botStyle();
    });
    
    function botStyle() {
        const estilo = document.createElement('link');
        estilo.rel = 'stylesheet';
        estilo.href = stylesBot;
        document.head.appendChild(estilo);
    }

    function injectStyles(iframeDocument) {
        const linkElement = iframeDocument.createElement('link');
        linkElement.rel = 'stylesheet';
        linkElement.href = stylesMsj; // Asegúrate de poner la ruta correcta
        iframeDocument.head.appendChild(linkElement);    
    }
    
    function injectScripts(iframeDocument) {

        // configuracion para MAthjax
        const mathjax = `MathJax.Hub.Config({tex2jax: {inlineMath: [['$','$'], ['\(','\)']]}});`
        const mathjax_config = iframeDocument.createElement("script");
        mathjax_config.type = "text/x-mathjax-config";
        mathjax_config.innerText = mathjax;
        iframeDocument.head.appendChild(mathjax_config);
        

        // script mathjax
        const mathjax_js = iframeDocument.createElement("script");
        mathjax_js.type = "text/javascript";
        mathjax_js.src = "https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.7/MathJax.js?config=TeX-MML-AM_CHTML";
        iframeDocument.head.appendChild(mathjax_js);

    }

    function sendQuestion() {
        const question = document.getElementById('inputQuestion').value;
        document.getElementById('inputQuestion').value = '';
    
        // Añadir la pregunta actual al historial de la conversación
        conversationHistory.push({ role: 'user', content: question });
    
        const iframe = document.getElementById('chatbotFrame');
        const iframeDocument = iframe.contentDocument || iframe.contentWindow.document;
    
        if (!iframeDocument.querySelector('style')) {
            injectStyles(iframeDocument);
        }

        if (!iframeDocument.querySelector('script')) {
            injectScripts(iframeDocument);
        }
    
    
        const userMessage = document.createElement('div');
        userMessage.className = 'message user-message';
        userMessage.innerHTML = `<strong>Usuario:</strong> ${question}`;
        iframeDocument.body.appendChild(userMessage);
    
        const loadingElement = document.createElement('div');
        loadingElement.id = 'loading';
        loadingElement.className = 'loading';
        iframeDocument.body.appendChild(loadingElement);
    
        scrollToBottom(iframe);
        
        fetch(api, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Cache-Control': 'no-cache'
                },
                body: JSON.stringify({
                    query: question,
                    history: conversationHistory,
                    bot: bot,
                    
                })
            })
            .then(response => response.json())
            .then(data => {
                // Eliminar el elemento de carga
                iframeDocument.getElementById('loading').remove();
    
                //agregar la respuesta al iframe
                const botMessage = document.createElement('div');
                botMessage.className = 'message bot-message';
                botMessage.id = "MathJax_Display";
                //botMessage.className = 'display: none;';
                botMessage.innerHTML = `<strong>${botName}:</strong> ${data.response}`;
                iframeDocument.body.appendChild(botMessage);

                 // Reprocesar MathJax
                if (iframeDocument.defaultView.MathJax) {
        iframeDocument.defaultView.MathJax.Hub.Queue(["Typeset", iframeDocument.defaultView.MathJax.Hub, botMessage]);
    }
                conversationHistory.push({ role: 'assistant', content: data.response });
    
                scrollToBottom(iframe);
            })
            .catch(error => {
                console.error('Error:', error);
                iframeDocument.getElementById('loading').remove();
            });
    }
    
    function toggleChatbot() {
        const chatbotContainer = document.getElementById('chatbot-container');
        const iframe = document.getElementById('chatbotFrame');
        if (chatbotContainer.style.display === 'none' || chatbotContainer.style.display === '') {
            chatbotContainer.style.display = 'block';
            scrollToBottom(iframe);
        } else {
            chatbotContainer.style.display = 'none';
        }
    }
    
    function scrollToBottom(iframe) {
        const iframeDocument = iframe.contentDocument || iframe.contentWindow.document;
        iframe.contentWindow.scrollTo(0, iframeDocument.body.scrollHeight);
    } 

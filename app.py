from flask import Flask, request, jsonify
from rembg import remove
import os
import requests
import uuid

app = Flask(__name__)

def download_image(url, filename):

    with open(filename, "wb") as f:

        response = requests.get(url)

        f.write(response.content)


@app.route('/remove_background', methods=['POST'])
def remove_image_background():

    try:
        image_url = request.form.get('image_url')

        if not image_url:

            return jsonify({"result": "error", "message": "URL da imagem não foi provida."}), 400

        # Cria o diretório "no-background" se não existir

        output_dir = "no-background"

        if not os.path.exists(output_dir):

            os.makedirs(output_dir)

        # Baixa a imagem da URL fornecida

        input_image_path = f"input_{uuid.uuid4().hex}.png"

        download_image(image_url, input_image_path)

        # Caminho de saída para a imagem sem fundo

        output_image_path = f"{output_dir}/output_{uuid.uuid4().hex}.png"

        # Remove o fundo da imagem

        with open(output_image_path, "wb") as f_output:

            f_output.write(remove(open(input_image_path, "rb").read()))

        # Remove o arquivo temporário de entrada

        os.remove(input_image_path)

        jls_extract_var = jsonify({"result": "success", "output_image_url": request.host_url + output_image_path})
        return jls_extract_var

    except Exception as e:

        return jsonify({"result": "error", "message": str(e)}), 500


if __name__ == '__main__':

    app.run(host='0.0.0.0', port=5000)

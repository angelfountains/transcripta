import streamlit as st
import whisper
import tempfile
from docx import Document

# Título de la aplicación
st.title("Transcripta")
st.subheader("Transcribe tus audios en segundos. Precisión, velocidad y simplicidad para cualquier necesidad.")

# Cargar archivo de audio
audio_file = st.file_uploader("Sube tu archivo de audio (MP3, WAV o M4A)", type=["mp3", "wav", "m4a"])

if audio_file is not None:
    with st.spinner("Transcribiendo..."):
        # Guardar temporalmente el archivo
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp_file:
            tmp_file.write(audio_file.read())
            tmp_file_path = tmp_file.name

        # Cargar modelo Whisper
        model = whisper.load_model("base")

        # Transcribir
        result = model.transcribe(tmp_file_path, language="es")
        transcripcion = result["text"]

        # Mostrar el texto
        st.success("¡Transcripción completa!")
        st.text_area("Texto transcrito:", transcripcion, height=300)

        # Botón para descargar como TXT
        st.download_button("Descargar como .txt", transcripcion, file_name="transcripcion.txt")

        # Botón para descargar como DOCX
        doc = Document()
        doc.add_heading("Transcripción", level=1)
        doc.add_paragraph(transcripcion)
        with tempfile.NamedTemporaryFile(delete=False, suffix=".docx") as tmp_docx:
            doc.save(tmp_docx.name)
            tmp_docx.seek(0)
            st.download_button("Descargar como .docx", tmp_docx.read(), file_name="transcripcion.docx")

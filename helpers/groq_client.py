"""
Module untuk integrasi dengan Groq API untuk chatbot dan ringkasan
"""

import logging
from typing import Dict, Any, List, Optional
from groq import Groq

from helpers.config import GROQ_API_KEY, GROQ_MODEL, CHATBOT_TEMPLATE

# Setup logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("groq_client")

client: Optional[Groq] = None


def create_groq_client() -> Optional[Groq]:
    """Create or reuse the Groq client using the configured API key."""
    global client
    if client is not None:
        return client

    if not GROQ_API_KEY:
        logger.error("GROQ_API_KEY is not set. Please configure the environment variable.")
        return None

    client = Groq(api_key=GROQ_API_KEY)
    return client


def check_groq_available() -> bool:
    """Check whether Groq API is configured and ready to use."""
    if not GROQ_API_KEY:
        logger.error("GROQ_API_KEY environment variable is missing.")
        return False
    return True


def generate_conclusion(
    description: str,
    sentiment_summary: str,
    model_name: str = GROQ_MODEL
) -> str:
    """
    Menghasilkan kesimpulan produk menggunakan model Groq API

    Args:
        description: Deskripsi produk
        sentiment_summary: Ringkasan sentimen
        model_name: Nama model untuk digunakan

    Returns:
        String kesimpulan produk
    """
    try:
        client = create_groq_client()
        if not client:
            return "Tidak dapat menghasilkan kesimpulan karena Groq API tidak dikonfigurasi."

        prompt = (
            "Kamu adalah asisten yang memberikan kesimpulan produk secara ringkas, objektif, dan alami berdasarkan data deskripsi dan sentimen.\n"
            "Buatkan kesimpulan apakah produk ini bagus dan worth it atau tidak, dengan gaya bahasa alami dan manusiawi. "
            "Gunakan informasi dari deskripsi dan ringkasan sentimen berikut.\n\n"
            f"Deskripsi produk:\n{description}\n\n"
            f"Ringkasan sentimen:\n{sentiment_summary}\n\n"
            "Berikan kesimpulan 3-5 kalimat, dengan bahasa Indonesia yang baik dan benar."
        )

        response = client.chat.completions.create(
            messages=[
                {"role": "user", "content": prompt}
            ],
            model=model_name,
            temperature=0.7,
            top_p=0.9,
        )

        if response and response.choices:
            return response.choices[0].message.content.strip() or "Tidak dapat menghasilkan kesimpulan."

        return "Tidak dapat menghasilkan kesimpulan."
    except Exception as e:
        logger.error(f"Error saat generate kesimpulan: {str(e)}")
        return "Tidak dapat menghasilkan kesimpulan karena error sistem."


def get_chat_response(
    user_question: str,
    product_data: Dict[str, Any],
    model_name: str = GROQ_MODEL
) -> str:
    """
    Mendapatkan respons chatbot dari model untuk pertanyaan pengguna

    Args:
        user_question: Pertanyaan pengguna
        product_data: Data produk lengkap
        model_name: Nama model untuk digunakan

    Returns:
        String respons dari chatbot
    """
    try:
        client = create_groq_client()
        if not client:
            return "Maaf, Groq API tidak dikonfigurasi."

        sample_reviews = []
        for i, review in enumerate(product_data.get('reviews', [])[:5]):
            sample_reviews.append(
                f"{i+1}. {review.get('Nama')}: \"{review.get('Ulasan')}\" (Rating: {review.get('Rating')}/5, Sentimen: {review.get('Sentimen')})"
            )

        prompt = CHATBOT_TEMPLATE.format(
            product_name=product_data.get('product_name', 'Produk tidak diketahui'),
            description=product_data.get('description', 'Deskripsi tidak tersedia'),
            review_count=len(product_data.get('reviews', [])),
            positive_count=product_data.get('sentiment_counts', {}).get('positive', 0),
            neutral_count=product_data.get('sentiment_counts', {}).get('neutral', 0),
            negative_count=product_data.get('sentiment_counts', {}).get('negative', 0),
            conclusion=product_data.get('conclusion', 'Kesimpulan tidak tersedia'),
            sample_reviews="\n".join(sample_reviews),
            user_question=user_question
        )

        response = client.chat.completions.create(
            messages=[
                {"role": "user", "content": prompt}
            ],
            model=model_name,
            temperature=0.8,
            top_p=0.9,
        )

        if response and response.choices:
            return response.choices[0].message.content.strip() or "Maaf, saya tidak dapat menjawab pertanyaan Anda saat ini."

        return "Maaf, saya tidak dapat menjawab pertanyaan Anda saat ini."
    except Exception as e:
        logger.error(f"Error saat generate chat response: {str(e)}")
        return "Maaf, terjadi kesalahan saat memproses pertanyaan Anda."


def setup_groq() -> bool:
    """
    Setup Groq client and ensure Groq API key is configured

    Returns:
        Boolean menandakan sukses atau gagal
    """
    if not check_groq_available():
        logger.error("Groq API key tidak dikonfigurasi. Silakan set GROQ_API_KEY environment variable.")
        return False

    if not create_groq_client():
        logger.error("Gagal membuat Groq client.")
        return False

    logger.info("Groq setup selesai, siap digunakan")
    return True

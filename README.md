#RentTech| AI-Enhanced Electronics Rental Platform 

## Abstract
This project proposes the development of a platform for renting electronic devices at affordable rates for predefined timeframes.  
It provides a streamlined solution for individuals and businesses needing temporary access to devices without purchasing them outright.  
Additionally, users can monetize unused devices by listing them for sale or rental.  

The platform integrates two main technologies:  
1. **AI-Powered Chatbot**: Provides quick, natural, and personalized responses using LLaMA 4 via OpenRouter API.  
2. **Sentiment Analysis**: Analyzes user reviews using Python and DistilBERT (Hugging Face) to gain insights and improve service quality.  

---

## Features
- Rent and list electronic devices with flexible timeframes.  
- AI chatbot for real-time user support.  
- Analyze customer feedback to improve services.  
- Role-based access for buyers, sellers, and managers.  
- Dynamic search and filters for devices.  
- Integration with Django Rest Framework API for seamless backend-frontend communication.  

---

## Software & Tools
- **Backend**: Python, Django  
- **Frontend**: HTML, CSS, JavaScript  
- **Database**: MySQL  
- **AI/ML**: Python (DistilBERT, Transformers, OpenRouter API)  
- **Other Tools**: Figma (UI Design), draw.io (UML), Microsoft Word (Documentation)

---

## Dataset
- **Tech Product Reviews Dataset** (from Mendeley Data)  
- 24,629 entries with product name, price, and review  
- Pre-processed and fine-tuned for DistilBERT sentiment analysis  

---

## How it Works
1. Users can rent or list devices.  
2. Comments/reviews are analyzed for sentiment (positive, negative, neutral).  
3. AI chatbot answers user inquiries in real-time.  
4. Admins can monitor feedback through dashboards.  
5. API endpoints provide structured data for frontend interactions.  

---

## Demo
[Watch the Demo Video](https://drive.google.com/file/d/1hxtEmmhAA9Wdm4ghyBhr8FFAmOMI5a-B/view?usp=sharing)  
---

## Installation
```bash
git clone https://github.com/RaghadTh24/AI-Enhanced_Electronics-_Rental_Platform.git
cd AI-Enhanced_Electronics-_Rental_Platform
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver


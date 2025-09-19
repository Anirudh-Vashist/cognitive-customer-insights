import pandas as pd
import matplotlib.pyplot as plt
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from django.conf import settings
import os

def sentiment_analysis(request):
    context = {}
    if request.method == 'POST' and request.FILES.get('csv_file'):
        csv_file = request.FILES['csv_file']
        fs = FileSystemStorage()
        filename = fs.save(csv_file.name, csv_file)
        file_path = fs.path(filename)

        df = pd.read_csv(file_path)

        # Check for required columns
        if 'sentiment' not in df.columns or 'sentence' not in df.columns:
            context['error'] = "CSV must contain 'sentence' and 'sentiment' columns."
            return render(request, 'index.html', context)

        # Optional: parse 'date' column
        if 'date' in df.columns:
            df['date'] = pd.to_datetime(df['date'], errors='coerce')
            df.dropna(subset=['date'], inplace=True)
            df['month'] = df['date'].dt.to_period('M')
        else:
            context['error'] = "CSV must contain a 'date' column for monthly trend."
            return render(request, 'index.html', context)

        # Bar chart: Sentiment Distribution
        sentiment_counts = df['sentiment'].value_counts()
        bar_chart_path = os.path.join(settings.MEDIA_ROOT, 'sentiment_bar.png')
        plt.figure(figsize=(6,4))
        sentiment_counts.plot(kind='bar', color=['green', 'red', 'gray'])
        plt.title('Sentiment Distribution')
        plt.xlabel('Sentiment')
        plt.ylabel('Count')
        plt.tight_layout()
        plt.savefig(bar_chart_path)
        plt.close()

        # Monthly Trend: count of each sentiment by month
        monthly_trend = df.groupby(['month', 'sentiment']).size().unstack(fill_value=0)
        monthly_trend.index = monthly_trend.index.astype(str)

        line_chart_path = os.path.join(settings.MEDIA_ROOT, 'monthly_sentiment_trend.png')
        monthly_trend.plot(figsize=(10,5), marker='o')
        plt.title('Monthly Sentiment Trend')
        plt.xlabel('Month')
        plt.ylabel('Count')
        plt.grid(True)
        plt.tight_layout()
        plt.savefig(line_chart_path)
        plt.close()

        loyalty_df = df[df['sentiment'].str.lower() == 'positive']
        loyalty_by_month = loyalty_df.groupby('month').size()
        loyalty_by_month.index = loyalty_by_month.index.astype(str)

        loyalty_chart_path = os.path.join(settings.MEDIA_ROOT, 'loyalty_chart.png')
        plt.figure(figsize=(8, 4))
        loyalty_by_month.plot(kind='bar', color='blue')
        plt.title('Monthly Customer Loyalty')
        plt.xlabel('Month')
        plt.ylabel('Loyal Customers')
        plt.tight_layout()
        plt.savefig(loyalty_chart_path)
        plt.close()

        context['loyalty_chart_url'] = fs.url('loyalty_chart.png')

        # Send data to template
        context['sentiment_table'] = df[['date', 'sentence', 'sentiment']].to_html(classes='table table-bordered', index=False)
        context['bar_chart_url'] = fs.url('sentiment_bar.png')
        context['monthly_line_chart_url'] = fs.url('monthly_sentiment_trend.png')

    return render(request, 'index.html', context)



 


import matplotlib
matplotlib.use('Agg')

import os
import pandas as pd
import pickle
from sklearn.cluster import KMeans, DBSCAN
from sklearn.preprocessing import StandardScaler, LabelEncoder
import matplotlib.pyplot as plt
from django.shortcuts import render, redirect
from django.core.files.storage import default_storage
from django.conf import settings

def dashboard(request):
    if request.method == 'POST':
        file = request.FILES['csv_file']
        file_name = default_storage.save(file.name, file)
        request.session['file_name'] = file_name
        return redirect('select_columns')
    return render(request, 'customer/dashboard.html')

def select_columns(request):
    file_name = request.session.get('file_name')
    if not file_name:
        return redirect('dashboard')
    
    # Load the uploaded CSV file
    data = pd.read_csv(default_storage.path(file_name))
    columns = data.columns.tolist()
    
    return render(request, 'customer/select_columns.html', {'columns': columns})

def results(request):
    if request.method == 'POST':
        file_name = request.session.get('file_name')
        selected_columns = request.POST.getlist('columns')
        
        # Load the uploaded CSV file
        data = pd.read_csv(default_storage.path(file_name))
        
        # Select only the user-selected columns
        data = data[selected_columns]

         # Convert categorical columns to numeric
        for col in data.select_dtypes(include=['object']).columns:
            if data[col].nunique() > 2:  
                # One-hot encoding for multi-category columns
                data = pd.get_dummies(data, columns=[col])
            else:  
                # Label encoding for binary categorical columns
                le = LabelEncoder()
                data[col] = le.fit_transform(data[col])

        
        # Preprocess the data (standardize for clustering)
        scaler = StandardScaler()
        scaled_data = scaler.fit_transform(data)
        
        # Perform K-Means clustering
        kmeans = KMeans(n_clusters=4, random_state=42)
        kmeans_labels = kmeans.fit_predict(scaled_data)
        
        # Perform DBSCAN clustering
        dbscan = DBSCAN(eps=0.5, min_samples=5)
        dbscan_labels = dbscan.fit_predict(scaled_data)

        static_dir = os.path.join(settings.BASE_DIR, 'static')
        if not os.path.exists(static_dir):
            os.makedirs(static_dir)
        
        # Create plots
        plt.figure(figsize=(10, 5))
        plt.scatter(data.iloc[:, 0], data.iloc[:, 1], c=kmeans_labels, cmap='viridis')
        plt.title('K-Means Clustering')
        plt.xlabel(selected_columns[0])
        plt.ylabel(selected_columns[1])
        kmeans_plot_path = 'static/kmeans_plot.png'
        plt.savefig(kmeans_plot_path)
        plt.close()
        
        plt.figure(figsize=(10, 5))
        plt.scatter(data.iloc[:, 0], data.iloc[:, 1], c=dbscan_labels, cmap='viridis')
        plt.title('DBSCAN Clustering')
        plt.xlabel(selected_columns[0])
        plt.ylabel(selected_columns[1])
        dbscan_plot_path = 'static/dbscan_plot.png'
        plt.savefig(dbscan_plot_path)
        plt.close()
        
        return render(request, 'customer/results.html', {
            'kmeans_plot': kmeans_plot_path,
            'dbscan_plot': dbscan_plot_path
        })
    return redirect('dashboard')


from django.http import JsonResponse

def cleanup_files(request):
    if request.method == 'POST':
        file_name = request.session.get('file_name')
        file_path = default_storage.path(file_name)

        # Paths to the generated images
        static_dir = os.path.join(settings.BASE_DIR, 'static')
        kmeans_plot_path = os.path.join(static_dir, 'kmeans_plot.png')
        dbscan_plot_path = os.path.join(static_dir, 'dbscan_plot.png')

        # Delete uploaded CSV file
        if file_name and os.path.exists(file_path):
            os.remove(file_path)

        # Delete generated images
        for plot_path in [kmeans_plot_path, dbscan_plot_path]:
            if os.path.exists(plot_path):
                os.remove(plot_path)

        # Clear session data
        request.session.pop('file_name', None)

        return JsonResponse({'status': 'success'})

    return JsonResponse({'status': 'error'}, status=400)

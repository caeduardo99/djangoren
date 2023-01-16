
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
import pandas as pd
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from plotly.offline import plot
import plotly.express as px
from datetime import datetime
from .models import Vgral

# Create your views here.


def home(request):
    return render(request, 'home.html', {
    })


@login_required
def dashboard(request):
    model = Vgral.objects.all()
    model_vendedor = Vgral.objects.values('nombrevend').order_by('nombrevend')
    model_vendedor = model_vendedor.distinct()
    model_prov = Vgral.objects.values(
        'nombreprovcli').order_by('nombreprovcli')
    model_prov = model_prov.distinct()
    model_line = Vgral.objects.values('desc_línea').order_by('desc_línea')
    model_line = model_line.distinct()
    modelGraf = Vgral.objects.all()
    vendedor_query = request.GET.getlist('vendedor')
    nomb_proveed_query = request.GET.getlist('proveedor')
    linea_query = request.GET.getlist('linea')
    date_since_query = request.GET.get('since')
    date_to_query = request.GET.get('to')
    
    # GRAFICOS
    projects_data = [
        {
            'Cantidad': x.cantidad,
            'NombreVendedor': x.nombrevend,
            'Precio Total': x.preciotreal,
            'Proveedor': x.nombreprovcli,
            'Utilidad': x.utilidad,
            'Costo Total Real': x.costototalreal,
            'Linea': x.desc_línea,
            'Item': x.descitem,
            'Fecha': x.fecha,
        } for x in modelGraf
    ]
    df = pd.DataFrame(projects_data)
    df1 = pd.DataFrame(df.groupby(by=['Fecha'])['Cantidad'].sum())
    fig = px.histogram(
        df, x='NombreVendedor', y=['Utilidad', 'Precio Total', 'Costo Total Real'], barmode='group',
    title='General')
    # CREACION DEL LAYOAUT PARA SELECCIONAR GRAFICOS
    fig.update_layout(
        updatemenus=[
            dict(
                buttons=list([
                    dict(
                        args=["type", "histogram"],
                        label="Histograma",
                        method="restyle"
                    ),
                    dict(
                        args=["type", "scatter"],
                        label="Lineas",
                        method="restyle"
                    ),
                    dict(
                        args=["type", "box"],
                        label="Cajas",
                        method="restyle"
                    )
                ]),
                direction="down",
            )
        ]
    )
    df1.reset_index(inplace=True)
    donut_fig = px.pie(df, values='Cantidad', names='NombreVendedor', hole=.3, title='General')
    fig_proov = px.scatter(df, x="Cantidad", y="Proveedor",
                           color='Linea', hover_name="Proveedor", title='General')
    
    fig_date = px.line(df1, x="Fecha", y="Cantidad")
    
    donut_fig.update_traces(textposition='inside')
    donut_fig.update_layout(uniformtext_minsize=12, uniformtext_mode='hide')
    
    gantt_plot = plot(fig, output_type="div")
    gantt_donut = plot(donut_fig, output_type="div")
    gantt_proov = plot(fig_proov, output_type="div")
    gantt_time_line = plot(fig_date, output_type="div")
# CONSULTAS -------------------------------------------------------------------------------------------------------------------
    data_frame_vendedor = pd.DataFrame()
    data_frame_proveedor = pd.DataFrame()
    data_frame_linea = pd.DataFrame()
    data_frame_date = pd.DataFrame()

    if vendedor_query != None and vendedor_query is not None:
        df_list = []
        for i in range(len(vendedor_query)):
            model_list = model.filter(nombrevend=vendedor_query[i])
            projects_data = [
                {
                    'Cantidad': x.cantidad,
                    'NombreVendedor': x.nombrevend,
                    'Precio Total': x.preciotreal,
                    'Proveedor': x.nombreprovcli,
                    'Utilidad': x.utilidad,
                    'Costo Total Real': x.costototalreal,
                    'Linea': x.desc_línea,
                    'Item': x.descitem,
                    'Fecha': x.fecha,
                }for x in model_list
            ]
            df_list.append(pd.DataFrame(projects_data))
            data_frame_vendedor = pd.concat(df_list, sort='False', ignore_index='True')
            fig = px.histogram(data_frame_vendedor, x='NombreVendedor', y=[
                           'Utilidad', 'Precio Total', 'Costo Total Real'], barmode='group', title=str(vendedor_query))
            fig.update_layout(
                updatemenus=[
                    dict(
                        buttons=list([
                            dict(
                                args=["type", "histogram"],
                                label="Histograma",
                                method="restyle"
                            ),
                            dict(
                                args=["type", "scatter"],
                                label="Lineas",
                                method="restyle"
                            ),
                            dict(
                                args=["type", "box"],
                                label="Cajas",
                                method="restyle"
                            )
                        ]),
                        direction="down"
                    )
                ]
            )
            donut_fig = px.pie(data_frame_vendedor, values='Cantidad', names='Linea',  hole=.3, title=str(vendedor_query))
            fig_proov = px.scatter(data_frame_vendedor, x="Cantidad", y="Proveedor",
                           color='Linea', hover_name="Proveedor", title=str(vendedor_query))
            fig_date = px.line(data_frame_vendedor, x="Fecha", y="Cantidad")
            donut_fig.update_traces(textposition='inside')
            donut_fig.update_layout(uniformtext_minsize=12, uniformtext_mode='hide')
            gantt_plot = plot(fig, output_type="div")
            gantt_donut = plot(donut_fig, output_type="div")
            gantt_proov = plot(fig_proov, output_type="div")
            gantt_time_line = plot(fig_date, output_type="div")
            
    # print(data_frame_vendedor)
    # CONSULTA DEL PROOVEDOR------------------------------------------------------
    if nomb_proveed_query != None and nomb_proveed_query is not None:
        df_list = []
        for i in range(len(nomb_proveed_query)):
            model_list = model.filter(nombreprovcli = nomb_proveed_query[i])
            projects_data = [
                {
                    'Cantidad': x.cantidad,
                    'NombreVendedor': x.nombrevend,
                    'Precio Total': x.preciotreal,
                    'Proveedor': x.nombreprovcli,
                    'Utilidad': x.utilidad,
                    'Costo Total Real': x.costototalreal,
                    'Linea': x.desc_línea,
                    'Item': x.descitem,
                    'Fecha': x.fecha,
                }for x in model_list
            ]
            df_list.append(pd.DataFrame(projects_data))
            data_frame_proveedor = pd.concat(df_list, sort='False', ignore_index='True')
            fig = px.histogram(data_frame_proveedor, x='NombreVendedor', y=[
                           'Utilidad', 'Precio Total', 'Costo Total Real'], barmode='group', title=str(nomb_proveed_query))
            fig.update_layout(
                updatemenus=[
                    dict(
                        buttons=list([
                            dict(
                                args=["type", "histogram"],
                                label="Histograma",
                                method="restyle"
                            ),
                            dict(
                                args=["type", "scatter"],
                                label="Lineas",
                                method="restyle"
                            ),
                            dict(
                                args=["type", "box"],
                                label="Histograma",
                                method="restyle"
                            )
                        ]),
                        direction="down"
                    )
                ]
            )
            donut_fig = px.pie(data_frame_proveedor, values='Cantidad', names='Linea',  hole=.3, title=str(nomb_proveed_query))
            fig_proov = px.scatter(data_frame_proveedor, x="Cantidad", y="Proveedor",
                           color='Linea', hover_name="Proveedor", title=str(nomb_proveed_query))
            fig_date = px.line(data_frame_proveedor, x="Fecha", y="Cantidad")
            donut_fig.update_traces(textposition='inside')
            donut_fig.update_layout(uniformtext_minsize=12, uniformtext_mode='hide')
            gantt_plot = plot(fig, output_type="div")
            gantt_donut = plot(donut_fig, output_type="div")
            gantt_proov = plot(fig_proov, output_type="div")
            gantt_time_line = plot(fig_date, output_type="div")
    
    # print(data_frame_proveedor)
    # CONSULTA DE LA LINEA-----------------------------------------------------
    if linea_query != None and linea_query is not None:
        df_list = []
        for  i in range(len(linea_query)):
            model_list = model.filter(desc_línea=linea_query[i])
            projects_data = [
                {
                    'Cantidad': x.cantidad,
                    'NombreVendedor': x.nombrevend,
                    'Precio Total': x.preciotreal,
                    'Proveedor': x.nombreprovcli,
                    'Utilidad': x.utilidad,
                    'Costo Total Real': x.costototalreal,
                    'Linea': x.desc_línea,
                    'Item': x.descitem,
                    'Fecha': x.fecha,
                }for x in model_list
            ]
            df_list.append(pd.DataFrame(projects_data))
            data_frame_linea = pd.concat(df_list, sort='False', ignore_index='True')
            
            fig = px.histogram(data_frame_linea, x='NombreVendedor', y=[
                           'Utilidad', 'Precio Total', 'Costo Total Real'], barmode='group', title=str(linea_query))
            fig.update_layout(
                updatemenus=[
                    dict(
                        buttons=list([
                            dict(
                                args=["type", "histogram"],
                                label="Histograma",
                                method="restyle"
                            ),
                            dict(
                                args=["type", "scatter"],
                                label="Lineas",
                                method="restyle"
                            ),
                            dict(
                                args=["type", "box"],
                                label="Histograma",
                                method="restyle"
                            )
                        ]),
                        direction="down"
                    )
                ]
            )
            donut_fig = px.pie(data_frame_linea, values='Cantidad', names='Linea', hole=.3, title=str(linea_query))
            fig_proov = px.scatter(data_frame_linea, x="Cantidad", y="Proveedor",
                           color='Linea', hover_name="Proveedor", title=str(linea_query))
            fig_date = px.line(data_frame_linea, x="Fecha", y="Cantidad")
            donut_fig.update_traces(textposition='inside')
            donut_fig.update_layout(uniformtext_minsize=12, uniformtext_mode='hide')
            gantt_plot = plot(fig, output_type="div")
            gantt_donut = plot(donut_fig, output_type="div")
            gantt_proov = plot(fig_proov, output_type="div")
            gantt_time_line = plot(fig_date, output_type="div")
            
    # print(data_frame_linea)
    
    # CONSULTAS CON LAS FECHAS
    if date_since_query != None and date_to_query != None:
        date_since = datetime.strptime(date_since_query, '%m/%d/%Y')
        date_to = datetime.strptime(date_to_query, '%m/%d/%Y')
        model_list = model.filter(fecha__range=(date_since,date_to))
        projects_data = [
                {
                    'Cantidad': x.cantidad,
                    'NombreVendedor': x.nombrevend,
                    'Precio Total': x.preciotreal,
                    'Proveedor': x.nombreprovcli,
                    'Utilidad': x.utilidad,
                    'Costo Total Real': x.costototalreal,
                    'Linea': x.desc_línea,
                    'Item': x.descitem,
                    'Fecha': x.fecha,
                }for x in model_list
            ]
        data_frame_date = pd.DataFrame(projects_data)
        df_sum = pd.DataFrame(data_frame_date.groupby(by=['Fecha'])['Cantidad'].sum())
        df_sum.reset_index(inplace=True)
        fig = px.histogram(data_frame_date, x='NombreVendedor', y=[
                           'Utilidad', 'Precio Total', 'Costo Total Real'], barmode='group', title=str([date_since_query, date_to_query]))
        fig.update_layout(
                updatemenus=[
                    dict(
                        buttons=list([
                            dict(
                                args=["type", "histogram"],
                                label="Histograma",
                                method="restyle"
                            ),
                            dict(
                                args=["type", "scatter"],
                                label="Lineas",
                                method="restyle"
                            ),
                            dict(
                                args=["type", "box"],
                                label="Histograma",
                                method="restyle"
                            )
                        ]),
                        direction="down"
                    )
                ]
            )
        donut_fig = px.pie(data_frame_date, values='Cantidad', names='Linea', hole=.3, title=str([date_since_query, date_to_query]))
        fig_proov = px.scatter(data_frame_date, x="Cantidad", y="Proveedor",
                           color='Linea', hover_name="Proveedor", title=str([date_since_query, date_to_query]))
        fig_date = px.line(df_sum, x='Fecha', y='Cantidad')
        donut_fig.update_traces(textposition='inside')
        donut_fig.update_layout(uniformtext_minsize=12, uniformtext_mode='hide')
        gantt_donut = plot(donut_fig, output_type="div")
        gantt_proov = plot(fig_proov, output_type="div")
        gantt_plot = plot(fig, output_type="div")
        gantt_time_line = plot(fig_date, output_type="div")
    # print(data_frame_date)
        
    if data_frame_vendedor.empty == False and data_frame_proveedor.empty == False:
        df_vend_prov = pd.merge(left=data_frame_vendedor, right=data_frame_proveedor, how='inner')
        fig = px.histogram(df_vend_prov, x='NombreVendedor', y=[
                           'Utilidad', 'Precio Total', 'Costo Total Real'], barmode='group')
        fig.update_layout(
                updatemenus=[
                    dict(
                        buttons=list([
                            dict(
                                args=["type", "histogram"],
                                label="Histograma",
                                method="restyle"
                            ),
                            dict(
                                args=["type", "scatter"],
                                label="Lineas",
                                method="restyle"
                            ),
                            dict(
                                args=["type", "box"],
                                label="Histograma",
                                method="restyle"
                            )
                        ]),
                        direction="down"
                    )
                ]
            )
        donut_fig = px.pie(df_vend_prov, values='Cantidad', names='Linea', hole=.3)
        fig_proov = px.scatter(df_vend_prov, x="Cantidad", y="Proveedor",
                           color='Linea', hover_name="Proveedor")
        fig_date = px.line(df_vend_prov, x="Fecha", y="Cantidad")
        donut_fig.update_traces(textposition='inside')
        donut_fig.update_layout(uniformtext_minsize=12, uniformtext_mode='hide')
        gantt_donut = plot(donut_fig, output_type="div")
        gantt_plot = plot(fig, output_type="div")
        gantt_proov = plot(fig_proov, output_type="div")
        gantt_time_line = plot(fig_date, output_type="div")
        
    if data_frame_vendedor.empty == False and data_frame_linea.empty == False:
        df_vend_line = pd.merge(left=data_frame_vendedor, right=data_frame_linea, how='inner')
        fig = px.histogram(df_vend_line, x='NombreVendedor', y=[
                           'Utilidad', 'Precio Total', 'Costo Total Real'], barmode='group')
        fig.update_layout(
                updatemenus=[
                    dict(
                        buttons=list([
                            dict(
                                args=["type", "histogram"],
                                label="Histograma",
                                method="restyle"
                            ),
                            dict(
                                args=["type", "scatter"],
                                label="Lineas",
                                method="restyle"
                            ),
                            dict(
                                args=["type", "box"],
                                label="Histograma",
                                method="restyle"
                            )
                        ]),
                        direction="down"
                    )
                ]
            )
        donut_fig = px.pie(df_vend_line, values='Cantidad', names='Item', hole=.3)
        fig_proov = px.scatter(df_vend_line, x="Cantidad", y="Proveedor",
                           color='Item', hover_name="Proveedor")
        fig_date = px.line(df_vend_line, x="Fecha", y="Cantidad")
        donut_fig.update_traces(textposition='inside')
        donut_fig.update_layout(uniformtext_minsize=12, uniformtext_mode='hide')
        gantt_plot = plot(fig, output_type="div")
        gantt_donut = plot(donut_fig, output_type="div")
        gantt_proov = plot(fig_proov, output_type="div")
        gantt_time_line = plot(fig_date, output_type="div")
    
    if data_frame_proveedor.empty == False and data_frame_linea.empty == False:
        df_pro_line = pd.merge(left=data_frame_proveedor, right=data_frame_linea, how='inner')
        fig = px.histogram(df_pro_line, x='NombreVendedor', y=[
                           'Utilidad', 'Precio Total', 'Costo Total Real'], barmode='group')
        fig.update_layout(
                updatemenus=[
                    dict(
                        buttons=list([
                            dict(
                                args=["type", "histogram"],
                                label="Histograma",
                                method="restyle"
                            ),
                            dict(
                                args=["type", "scatter"],
                                label="Lineas",
                                method="restyle"
                            ),
                            dict(
                                args=["type", "box"],
                                label="Histograma",
                                method="restyle"
                            )
                        ]),
                        direction="down"
                    )
                ]
            )
        donut_fig = px.pie(df_pro_line, values='Cantidad', names='Item', hole=.3)
        fig_proov = px.scatter(df_pro_line, x="Cantidad", y="Proveedor",
                           color='Linea', hover_name="Proveedor")
        fig_date = px.line(df_pro_line, x="Fecha", y="Cantidad")
        donut_fig.update_traces(textposition='inside')
        donut_fig.update_layout(uniformtext_minsize=12, uniformtext_mode='hide')
        gantt_plot = plot(fig, output_type="div")
        gantt_donut = plot(donut_fig, output_type="div")
        gantt_proov = plot(fig_proov, output_type="div")
        gantt_time_line = plot(fig_date, output_type="div")
    
    if data_frame_vendedor.empty == False and data_frame_proveedor.empty == False and data_frame_linea.empty == False:
        df_vendedor_prov = pd.merge(left=data_frame_vendedor, right=data_frame_proveedor, how='inner')
        df_vend_prov_line = pd.merge(left=df_vendedor_prov, right=data_frame_linea, how='inner')
        fig = px.histogram(df_vend_prov_line, x='NombreVendedor', y=[
                           'Utilidad', 'Precio Total', 'Costo Total Real'], barmode='group')
        fig.update_layout(
                updatemenus=[
                    dict(
                        buttons=list([
                            dict(
                                args=["type", "histogram"],
                                label="Histograma",
                                method="restyle"
                            ),
                            dict(
                                args=["type", "scatter"],
                                label="Lineas",
                                method="restyle"
                            ),
                            dict(
                                args=["type", "box"],
                                label="Histograma",
                                method="restyle"
                            )
                        ]),
                        direction="down"
                    )
                ]
            )
        donut_fig = px.pie(df_vend_prov_line, values='Cantidad', names='Item', hole=.3)
        fig_proov = px.scatter(df_vend_prov_line, x="Cantidad", y="Proveedor",
                           color='Linea', hover_name="Proveedor")
        fig_date = px.line(df_vend_prov_line, x="Fecha", y="Cantidad")
        donut_fig.update_traces(textposition='inside')
        donut_fig.update_layout(uniformtext_minsize=12, uniformtext_mode='hide')
        gantt_donut = plot(donut_fig, output_type="div")
        gantt_plot = plot(fig, output_type="div")
        gantt_proov = plot(fig_proov, output_type="div")
        gantt_time_line = plot(fig_date, output_type="div")

    if data_frame_date.empty == False and data_frame_vendedor.empty == False:
        df_date_vend = pd.merge(left=data_frame_date, right=data_frame_vendedor, how='inner')
        df_date_vend_sum = pd.DataFrame(df_date_vend.groupby(by=['Fecha'])['Cantidad'].sum())
        df_date_vend_sum.reset_index(inplace=True)
        
        fig = px.histogram(df_date_vend, x='NombreVendedor', y=[
                           'Utilidad', 'Precio Total', 'Costo Total Real'], barmode='group')
        fig.update_layout(
                updatemenus=[
                    dict(
                        buttons=list([
                            dict(
                                args=["type", "histogram"],
                                label="Histograma",
                                method="restyle"
                            ),
                            dict(
                                args=["type", "scatter"],
                                label="Lineas",
                                method="restyle"
                            ),
                            dict(
                                args=["type", "box"],
                                label="Cajas",
                                method="restyle"
                            )
                        ]),
                        direction="down"
                    )
                ]
            )
        donut_fig = px.pie(df_date_vend, values='Cantidad', names='Item', hole=.3)
        fig_proov = px.scatter(df_date_vend, x="Cantidad", y="Proveedor",
                           color='Linea', hover_name="Proveedor")
        fig_date=px.line(df_date_vend_sum, x='Fecha', y='Cantidad')
        donut_fig.update_traces(textposition='inside')
        donut_fig.update_layout(uniformtext_minsize=12, uniformtext_mode='hide')
        gantt_plot = plot(fig, output_type="div")
        gantt_donut = plot(donut_fig, output_type="div")
        gantt_proov = plot(fig_proov, output_type="div")
        gantt_time_line = plot(fig_date, output_type="div")
    
    if data_frame_date.empty == False and data_frame_proveedor.empty == False:
        df_date_prov = pd.merge(left=data_frame_date, right=data_frame_proveedor, how='inner')
        df_sum = pd.DataFrame(df_date_prov.groupby(by=['Fecha'])['Cantidad'].sum())
        df_sum.reset_index(inplace=True)
        fig = px.histogram(df_date_prov, x='NombreVendedor', y=[
                           'Utilidad', 'Precio Total', 'Costo Total Real'], barmode='group')
        fig.update_layout(
                updatemenus=[
                    dict(
                        buttons=list([
                            dict(
                                args=["type", "histogram"],
                                label="Histograma",
                                method="restyle"
                            ),
                            dict(
                                args=["type", "scatter"],
                                label="Lineas",
                                method="restyle"
                            ),
                            dict(
                                args=["type", "box"],
                                label="Histograma",
                                method="restyle"
                            )
                        ]),
                        direction="down"
                    )
                ]
            )
        donut_fig = px.pie(df_date_prov, values='Cantidad', names='Item', hole=.3)
        fig_proov = px.scatter(df_date_prov, x="Cantidad", y="Proveedor",
                           color='Linea', hover_name="Proveedor")
        fig_date = px.line(df_sum, x='Fecha', y='Cantidad')
        donut_fig.update_traces(textposition='inside')
        donut_fig.update_layout(uniformtext_minsize=12, uniformtext_mode='hide')
        gantt_plot = plot(fig, output_type="div")
        gantt_donut = plot(donut_fig, output_type="div")
        gantt_proov = plot(fig_proov, output_type="div")
        gantt_time_line = plot(fig_date, output_type="div")
    
    if data_frame_date.empty == False and data_frame_linea.empty == False:
        df_date_linea = pd.merge(left=data_frame_date, right=data_frame_linea, how='inner')
        df_sum = pd.DataFrame(df_date_linea.groupby(by=['Fecha'])['Cantidad'].sum())
        df_sum.reset_index(inplace=True)
        fig = px.histogram(df_date_linea, x='NombreVendedor', y=[
                           'Utilidad', 'Precio Total', 'Costo Total Real'], barmode='group')
        fig.update_layout(
                updatemenus=[
                    dict(
                        buttons=list([
                            dict(
                                args=["type", "histogram"],
                                label="Histograma",
                                method="restyle"
                            ),
                            dict(
                                args=["type", "scatter"],
                                label="Lineas",
                                method="restyle"
                            ),
                            dict(
                                args=["type", "box"],
                                label="Histograma",
                                method="restyle"
                            )
                        ]),
                        direction="down"
                    )
                ]
            )
        donut_fig = px.pie(df_date_linea, values='Cantidad', names='Item', hole=.3)
        fig_proov = px.scatter(df_date_linea, x="Cantidad", y="Proveedor",
                           color='Linea', hover_name="Proveedor")
        fig_date = px.line(df_sum, x='Fecha', y='Cantidad')
        donut_fig.update_traces(textposition='inside')
        donut_fig.update_layout(uniformtext_minsize=12, uniformtext_mode='hide')
        gantt_plot = plot(fig, output_type="div")
        gantt_donut = plot(donut_fig, output_type="div")
        gantt_proov = plot(fig_proov, output_type="div")
        gantt_time_line = plot(fig_date, output_type="div")
    
    if data_frame_date.empty == False and data_frame_vendedor.empty == False  and data_frame_proveedor.empty == False:
        df_vend_prov = pd.merge(left=data_frame_vendedor, right=data_frame_proveedor, how='inner')
        df_date_vend_prov = pd.merge(left=df_vend_prov, right=data_frame_date, how='inner')
        df_sum = pd.DataFrame(df_date_vend_prov.groupby(by=['Fecha'])['Cantidad'].sum())
        df_sum.reset_index(inplace=True)
        fig = px.histogram(df_date_vend_prov, x='NombreVendedor', y=[
                           'Utilidad', 'Precio Total', 'Costo Total Real'], barmode='group')
        fig.update_layout(
                updatemenus=[
                    dict(
                        buttons=list([
                            dict(
                                args=["type", "histogram"],
                                label="Histograma",
                                method="restyle"
                            ),
                            dict(
                                args=["type", "scatter"],
                                label="Lineas",
                                method="restyle"
                            ),
                            dict(
                                args=["type", "box"],
                                label="Histograma",
                                method="restyle"
                            )
                        ]),
                        direction="down"
                    )
                ]
            )
        donut_fig = px.pie(df_date_vend_prov, values='Cantidad', names='Item', hole=.3)
        fig_proov = px.scatter(df_date_vend_prov, x="Cantidad", y="Proveedor",
                           color='Linea', hover_name="Proveedor")
        fig_date = px.line(df_sum, x='Fecha', y='Cantidad')
        donut_fig.update_traces(textposition='inside')
        donut_fig.update_layout(uniformtext_minsize=12, uniformtext_mode='hide')
        gantt_donut = plot(donut_fig, output_type="div")
        gantt_plot = plot(fig, output_type="div")
        gantt_proov = plot(fig_proov, output_type="div")
        gantt_time_line = plot(fig_date, output_type="div")
    
    if data_frame_date.empty == False and data_frame_vendedor.empty == False and data_frame_linea.empty == False:
        df_vend_linea = pd.merge(left=data_frame_vendedor, right=data_frame_linea, how='inner')
        df_date_ven_linea = pd.merge(left=df_vend_linea, right=data_frame_date, how='inner')
        df_sum = pd.DataFrame(df_date_ven_linea.groupby(by=['Fecha'])['Cantidad'].sum())
        df_sum.reset_index(inplace=True)
        fig = px.histogram(df_date_ven_linea, x='NombreVendedor', y=[
                           'Utilidad', 'Precio Total', 'Costo Total Real'], barmode='group')
        fig.update_layout(
                updatemenus=[
                    dict(
                        buttons=list([
                            dict(
                                args=["type", "histogram"],
                                label="Histograma",
                                method="restyle"
                            ),
                            dict(
                                args=["type", "scatter"],
                                label="Lineas",
                                method="restyle"
                            ),
                            dict(
                                args=["type", "box"],
                                label="Histograma",
                                method="restyle"
                            )
                        ]),
                        direction="down"
                    )
                ]
            )
        donut_fig = px.pie(df_date_ven_linea, values='Cantidad', names='Item', hole=.3)
        fig_proov = px.scatter(df_date_ven_linea, x="Cantidad", y="Proveedor",
                           color='Linea', hover_name="Proveedor")
        fig_date = px.line(df_sum, x='Fecha', y='Cantidad')
        donut_fig.update_traces(textposition='inside')
        donut_fig.update_layout(uniformtext_minsize=12, uniformtext_mode='hide')
        gantt_donut = plot(donut_fig, output_type="div")
        gantt_plot = plot(fig, output_type="div")
        gantt_proov = plot(fig_proov, output_type="div")
        gantt_time_line = plot(fig_date, output_type="div")
    
    if data_frame_date.empty == False and data_frame_proveedor.empty == False and data_frame_linea.empty == False:
        df_prov_linea = pd.merge(left=data_frame_proveedor, right=data_frame_linea, how='inner')
        df_date_prov_linea = pd.merge(left=df_prov_linea, right=data_frame_date, how='inner')
        df_suma = pd.DataFrame(df_date_prov_linea.groupby(by=['Fecha'])['Cantidad'].sum())
        df_suma.reset_index(inplace=True)
        fig = px.histogram(df_date_prov_linea, x='NombreVendedor', y=[
                           'Utilidad', 'Precio Total', 'Costo Total Real'], barmode='group')
        fig.update_layout(
                updatemenus=[
                    dict(
                        buttons=list([
                            dict(
                                args=["type", "histogram"],
                                label="Histograma",
                                method="restyle"
                            ),
                            dict(
                                args=["type", "scatter"],
                                label="Lineas",
                                method="restyle"
                            ),
                            dict(
                                args=["type", "box"],
                                label="Histograma",
                                method="restyle"
                            )
                        ]),
                        direction="down"
                    )
                ]
            )
        donut_fig = px.pie(df_date_prov_linea, values='Cantidad', names='Item', hole=.3)
        fig_proov = px.scatter(df_date_prov_linea, x="Cantidad", y="Proveedor",
                           color='Linea', hover_name="Proveedor")
        fig_date = px.line(df_suma, x='Fecha', y='Cantidad')
        donut_fig.update_traces(textposition='inside')
        donut_fig.update_layout(uniformtext_minsize=12, uniformtext_mode='hide')
        gantt_donut = plot(donut_fig, output_type="div")
        gantt_plot = plot(fig, output_type="div")
        gantt_proov = plot(fig_proov, output_type="div")
        gantt_time_line = plot(fig_date, output_type="div")
    
    if data_frame_date.empty == False and data_frame_vendedor.empty == False and data_frame_proveedor.empty == False and data_frame_linea.empty == False:
        df_vend_prov = pd.merge(left=data_frame_vendedor, right=data_frame_proveedor, how='inner')
        df_vend_prov_linea = pd.merge(left=df_vend_prov, right=data_frame_linea, how='inner')
        df_vend_prov_linea_date = pd.merge(left=df_vend_prov_linea, right=data_frame_date, how='inner')
        df_sum = pd.DataFrame(df_vend_prov_linea_date.groupby(by=['Fecha'])['Cantidad'].sum())
        df_sum.reset_index(inplace=True)
        fig = px.histogram(df_vend_prov_linea_date, x='NombreVendedor', y=[
                           'Utilidad', 'Precio Total', 'Costo Total Real'], barmode='group')
        fig.update_layout(
                updatemenus=[
                    dict(
                        buttons=list([
                            dict(
                                args=["type", "histogram"],
                                label="Histograma",
                                method="restyle"
                            ),
                            dict(
                                args=["type", "scatter"],
                                label="Lineas",
                                method="restyle"
                            ),
                            dict(
                                args=["type", "box"],
                                label="Histograma",
                                method="restyle"
                            )
                        ]),
                        direction="down"
                    )
                ]
            )
        donut_fig = px.pie(df_vend_prov_linea_date, values='Cantidad', names='Item', hole=.3)
        fig_proov = px.scatter(df_vend_prov_linea_date, x="Cantidad", y="Proveedor",
                           color='Linea', hover_name="Proveedor")
        fig_date = px.line(df_sum, x='Fecha', y='Cantidad')
        donut_fig.update_traces(textposition='inside')
        donut_fig.update_layout(uniformtext_minsize=12, uniformtext_mode='hide')
        gantt_donut = plot(donut_fig, output_type="div")
        gantt_plot = plot(fig, output_type="div")
        gantt_proov = plot(fig_proov, output_type="div")
        gantt_time_line = plot(fig_date, output_type="div")

    
    context = {
        'queryset': model,
        'plot_div': gantt_plot,
        'donut': gantt_donut,
        'provee': gantt_proov,
        'check_prov': model_prov,
        'check_linea': model_line,
        'check_vendedor': model_vendedor,
        'time_line': gantt_time_line
    }
    
    # RENDERIZACION DEL LA PAGINA
    return render(request, 'dashboard.html', context)


def signup(request):

    if request.method == 'GET':
        return render(request, 'signup.html', {
            'form': UserCreationForm
        })
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(
                    username=request.POST["username"], password=request.POST["password1"])
                user.save()
                return HttpResponse('Usuario registrado exitosamente')
            except:
                return render(request, 'signup.html', {
                    'form': UserCreationForm,
                    'error': 'El usuario ya existe'
                })
        return render(request, 'signup.html', {
            'form': UserCreationForm,
            'error': 'las contraseñas no coinciden'
        })


@login_required
def signout(request):
    logout(request)
    return redirect('home')


def signin(request):
    if request.method == 'GET':
        return render(request, 'signin.html', {
            "form": AuthenticationForm
        })
    else:
        user = authenticate(
            request, username=request.POST['username'], password=request.POST
            ['password'])
        if user is None:
            return render(request, 'signin.html', {
                "form": AuthenticationForm,
                "error": "Username or password is incorrect."
            })
        login(request, user)
        return redirect('dashboard')

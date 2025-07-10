import pandas as pd
import numpy as np 

clientes = pd.read_csv(r'C:\Users\LENOVO\Desktop\Tripleten-DA\SPRT_7\PRÁCTICAS\datos_exámen\datos_clientes.csv')
fechas= pd.read_csv(r"C:\Users\LENOVO\Desktop\Tripleten-DA\SPRT_7\PRÁCTICAS\datos_exámen\DATOS_fechas.csv")
transacciones = pd.read_csv(r"C:\Users\LENOVO\Desktop\Tripleten-DA\SPRT_7\PRÁCTICAS\datos_exámen\DATOS_transacciones.csv")

#¿Quien es el cliente con la mayor cantidad de StockCode?
transacciones ['customer_id_int'] = transacciones['CustomerID'].astype('int') 
cliente_sc = transacciones.groupby('customer_id_int')['StockCode'].count().sort_values(ascending=False).reset_index()
transacciones_with_cliente= cliente_sc.merge(clientes, left_on= 'customer_id_int', right_on = 'CustomerID' )
#print('El cliente con la mayor cantidad de StockCode es:',transacciones_with_cliente.head(1))
#Con los datos de nuestros clientes, ¿cual es la edad promedio de nuestros clientes?
#print('La edad promedio de los clientes es:',clientes['Edad'].mean())
#¿Cuantos clientes tenemos con nombres repetidos y con nombres únicos?
nombres_repetidos= clientes['Nombre'].duplicated().sum()
nombres_unicos = clientes['Nombre'].nunique()
#print('Nombres repetidos:',nombres_repetidos, ', nombres únicos:', nombres_unicos)
#¿Quien es el cliente que más compra ha hecho segun nuestra base de datos de fechas y cual es el més en que mayor cantidad de compras hizo?
fechas['FechaCompra']=pd.to_datetime(fechas['FechaCompra'])
fechas['mes'] = fechas['FechaCompra'].dt.month
mayor_n_ventas=fechas.groupby('CustomerID')['CustomerID'].count().sort_values(ascending=False)
ventas_por_mes= fechas.query('CustomerID == 103')[['CustomerID', 'mes']].value_counts().reset_index()
#print('Cliente con el mayor número de compras:', mayor_n_ventas.head(1), 'el mes con mayor número de compras fue:', ventas_por_mes['mes'].head(1))
#Van a crear un nuevo DataFrame con la siguiente info: Nombre, Edad, StockCode, Description y Quantity. Estos nuevos DataFrames deben ser coherentes con los datos ya entregados.
clientes_filtrado= clientes[['Nombre','Edad','CustomerID']]
transacciones_filtrado = transacciones[['customer_id_int','StockCode','Description','Quantity']]
nuevo_df = clientes_filtrado.merge(transacciones_filtrado, left_on='CustomerID', right_on='customer_id_int')
nuevo_df =nuevo_df.drop('customer_id_int',axis ='columns')
#Con el DataFrame anterior van a crear dos columnas nuevas que son: grupo_edad y grupo_cantidad
bins = [0, 18, 35, 60, 100]  # límites de edad
labels = ['Adolescente', 'Joven adulto', 'Adulto', 'Adulto mayor']
nuevo_df['grupo_edad'] = pd.cut(nuevo_df['Edad'], bins=bins, labels=labels)

bins = [0, 5, 8, 20]  # límites de edad
labels = ['Mirón', 'básico', 'Premium']
nuevo_df['grupo_cantidad'] = pd.cut(nuevo_df['Quantity'], bins=bins, labels=labels)
print(nuevo_df)
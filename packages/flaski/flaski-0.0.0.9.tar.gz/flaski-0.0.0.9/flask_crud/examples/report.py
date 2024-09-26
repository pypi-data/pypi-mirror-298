from flask import Flask, render_template, redirect, url_for, request, session, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_mysqldb import MySQL
from config import Config
import hashlib
from models import Usuario, Venta

@app.route('/export_reportes/<formato>', methods=['GET'])
def export_reportes(formato):
    # Obtener los reportes de la base de datos
    cur = mysql.connection.cursor()
    cur.execute("SELECT categoria, SUM(cantidad) as total_cantidad, SUM(cantidad * precio) as total_venta FROM ventas GROUP BY categoria")
    reportes = cur.fetchall()
    cur.close()

    # Convertir reportes a DataFrame de pandas
    df = pd.DataFrame(reportes, columns=['Categoría', 'Total Cantidad', 'Total Venta'])

    if formato == 'csv':
        output = io.StringIO()
        df.to_csv(output, index=False)
        output.seek(0)
        return send_file(io.BytesIO(output.getvalue().encode()), mimetype='text/csv', as_attachment=True, download_name='reportes.csv')
    elif formato == 'xls':
        output = io.BytesIO()
        writer = pd.ExcelWriter(output, engine='xlsxwriter')
        df.to_excel(writer, index=False, sheet_name='Reportes')
        writer.close()
        output.seek(0)
        return send_file(output, mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', as_attachment=True, download_name='reportes.xlsx')
    elif formato == 'json':
        output = df.to_json(orient='records')
        return send_file(io.BytesIO(output.encode()), mimetype='application/json', as_attachment=True, download_name='reportes.json')
    elif formato == 'pdf':
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        
        # Header
        pdf.cell(200, 10, txt="Reportes de Ventas", ln=True, align='C')
        
        # Table
        pdf.set_font("Arial", size=10)
        col_width = pdf.w / 4.5
        row_height = pdf.font_size
        spacing = 1.5
        for row in reportes:
            for item in row:
                pdf.cell(col_width, row_height * spacing, txt=str(item), border=1)
            pdf.ln(row_height * spacing)
        
        output = io.BytesIO()
        pdf.output(dest='S').encode('latin1')
        output.write(pdf.output(dest='S').encode('latin1'))
        #pdf.output(output)
        output.seek(0)
        return send_file(output, mimetype='application/pdf', as_attachment=True, download_name='reportes.pdf')
    else:
        return "Formato no soportado", 400

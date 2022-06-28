from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from sqlalchemy import desc
import json
import requests
#import viacep


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///equipamentos.sqlite3'
db = SQLAlchemy(app)

class Equipamento(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(100), nullable=False)
    consumo = db.Column(db.Integer, nullable=False)
    tempo = db.Column(db.Integer, nullable=False)

    def __init__(self, nome, consumo, tempo):
        self.nome = nome 
        self.consumo = consumo
        self.tempo = tempo 

@app.route("/")
def index():
    equipamentos = Equipamento.query.all()
    return render_template('index.html', equipamentos=equipamentos)

@app.route('/new', methods=['GET','POST'])
def new():
    if request.method == 'POST':
        equipamento = Equipamento(
            request.form['nome'],
            request.form['consumo'],
            request.form['tempo']
        )
        db.session.add(equipamento)
        db.session.commit()
    return render_template('new.html')


#@app.route('/cep', methods=['POST'])
#def CEP():
#    d_cep = request.form['cep']
#    d = viacep.ViaCEP(d_cep)
#    dados_json = d.getDadosCEP()
#
#    cep      = dados_json['cep']
#    rua      = (u'%s' % dados_json['logradouro'])
#    bairro   = (u'%s' % dados_json['bairro'])
#    cidade   = (u'%s' % dados_json['cidade'])
#    uf       = dados_json['uf']
#    return render_template('cep.html', cep=cep,rua=rua,bairro=bairro,cidade=cidade,uf=uf)


@app.route('/cep')
def CEP():
    return render_template("cep.html")

@app.route("/resp")
def resp():
    equipamentos = Equipamento.query.all()
    un = db.session.query(Equipamento.nome).filter(Equipamento.id == db.session.query(func.max(Equipamento.id))).scalar()
    uc = db.session.query(Equipamento.consumo).filter(Equipamento.id == db.session.query(func.max(Equipamento.id))).scalar()
    ut = db.session.query(Equipamento.tempo).filter(Equipamento.id == db.session.query(func.max(Equipamento.id))).scalar()
    meduc = round(uc / ut)
    sumcotv = db.session.query(func.sum(Equipamento.consumo)).filter(Equipamento.nome=='Televisão').scalar()
    sumtetv = db.session.query(func.sum(Equipamento.tempo)).filter(Equipamento.nome=='Televisão').scalar()
    medtv = round(sumcotv / sumtetv)
    sumcoge = db.session.query(func.sum(Equipamento.consumo)).filter(Equipamento.nome=='Geladeira').scalar()
    sumtege = db.session.query(func.sum(Equipamento.tempo)).filter(Equipamento.nome=='Geladeira').scalar()
    medge = round(sumcoge / sumtege)
    sumcolr = db.session.query(func.sum(Equipamento.consumo)).filter(Equipamento.nome=='Lava Roupas').scalar()
    sumtelr = db.session.query(func.sum(Equipamento.tempo)).filter(Equipamento.nome=='Lava Roupas').scalar()
    medlr = round(sumcolr / sumtelr)
    sumcomo = db.session.query(func.sum(Equipamento.consumo)).filter(Equipamento.nome=='Microondas').scalar()
    sumtemo = db.session.query(func.sum(Equipamento.tempo)).filter(Equipamento.nome=='Microondas').scalar()
    medmo = round(sumcomo / sumtemo)
    sumcoac = db.session.query(func.sum(Equipamento.consumo)).filter(Equipamento.nome=='Ar Condicionado').scalar()
    sumteac = db.session.query(func.sum(Equipamento.tempo)).filter(Equipamento.nome=='Ar Condicionado').scalar()
    medac = round(sumcoac / sumteac)
    if (un == 'Televisão') and (meduc > medtv):
        conc = "O consumo de sua televisão está acima da média!"
    if (un == 'Televisão') and (meduc <= medtv):
        conc = "O consumo de sua televisão está dentro do esperado!"
    if (un == 'Geladeira') and (meduc > medge):
        conc = "O consumo de sua geladeira está acima da média!"
    if (un == 'Geladeira') and (meduc <= medge):
        conc = "O consumo de sua geladeira está dentro do esperado!"
    if (un == 'Lava Roupas') and (meduc > medlr):
        conc = "O consumo de sua Lava Roupas está acima da média!"
    if (un == 'Lava Roupas') and (meduc <= medlr):
        conc = "O consumo de sua Lava Roupas está dentro do esperado!"
    if (un == 'Microondas') and (meduc > medmo):
        conc = "O consumo de seu Micro-ondas está acima da média!"
    if (un == 'Microondas') and (meduc <= medmo):
        conc = "O consumo de seu Micro-ondas está dentro do esperado!"
    if (un == 'Ar Condicionado') and (meduc > medac):
        conc = "O consumo de seu Ar Condicionado está acima da média!"
    if (un == 'Ar Condicionado') and (meduc <= medac):
        conc = "O consumo de seu Ar Condicionado está dentro do esperado!"
    return render_template('resp.html', conc=conc, un=un, meduc=meduc, medtv=medtv, equipamentos=equipamentos, medge=medge, medlr=medlr, medmo=medmo, medac=medac)


if __name__ =='__main__':
    db.create_all()
    app.run(debug=True)
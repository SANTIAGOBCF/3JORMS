#post

@app.route('/report', methods = ['POST','GET'])
def report():
    action = request.args.get('action') # report/ignore/delete
    postType = request.args.get('postType')
    postId = request.args.get('postId')
    if (postType == 'post'):
        rPost = Publicaciones.query.filter_by(id = postId).first()
        if (action == 'report'):
            rPost.reportado = True
            chosenReason = request.form['optradio']
            rPost.reason = chosenReason
            if (chosenReason == 'Other' and chosenReason != ''):
                rPost.reason = request.form['other_text']
        elif (action == 'ignore'):
            rPost.reportado = False
        elif (action == 'delete'):
            db2.session.delete(rPost)
        db2.session.commit()
    elif (postType == 'character'):
        rCharacter = Personajes.query.filter_by(id = postId).first()
        if (action == 'report'):
            rCharacter.reportado = True
            chosenReason = request.form['optradio']
            rCharacter.reason = chosenReason
            if (chosenReason == 'Other' and chosenReason != ''):
                rCharacter.reason = request.form['other_text']
        elif (action == 'ignore'):
            rCharacter.reportado = False
        elif (action == 'delete'):
            charPosts = Publicaciones.query.filter(Publicaciones.personaje == rCharacter.nombre)
            db.session.delete(rCharacter)
            for charPost in charPosts:
                db2.session.delete(charPost)
            db2.session.commit()
        db.session.commit()
    if (action == 'report'):
        return '''
        <script> window.alert("Publicación reportada"); </script>
        <script> window.history.back(); </script>'''
    else:
        return '''<script> window.location=document.referrer; </script>'''

@app.route('/postspersonaje', methods = ['POST','GET'])
def characterPosts():
    name = request.args.get('name')
    postId = request.args.get('id')
    personaje = Personajes.query.filter_by(id = postId).first()
    post = Publicaciones.query.filter_by(personaje = name)
    return render_template('personaj.html', posts = post, personaje = personaje)

@app.route('/login',methods = ['POST','GET'])
def login():
    if(request.method == "GET"):
        if 'name' in session:
            return redirect(url_for('editor'))
    else:
        #obtiene datos 
        correo = request.form['username']
        password = request.form['password']
        password_encode = password.encode("utf-8")
        usuario = Usuarios.query.filter_by(correo = correo).first()
        if(usuario != None):
            #obtiene el password encriptado encode
            password_encriptado_encode = usuario.contraseña
            #verifica el password
            if(bcrypt.checkpw(password_encode,password_encriptado_encode)):
                #registra la sesion
                if (usuario.rol != 'VETADO'):
                    session['name'] = usuario.nombre      
                    session['rol'] = usuario.rol
                    session['logged_in'] = True
                    return redirect(url_for('index'))
                return '''
        <script> window.alert("Su cuenta ha sido vetada."); </script>
        <script> window.location=document.referrer; </script>'''
    return render_template('login.html')

@app.route('/editor-usuario', methods = ['POST','GET'])
def editor():
    if(request.method == "GET"):
        if 'name' in session:
            tasks = Usuarios.query.filter_by(nombre = session['name']).first()
            return render_template('editor-usuario.html', tasks = tasks)
        else:
            return redirect(url_for('ingresar'))
    else:
        if 'name' in session:
            tasks = Usuarios.query.filter_by(nombre = session['name']).first()
            if(request.form['nombre']!=''):
                nombre =request.form['nombre']
                tasks.nombre = nombre
                if(tasks.foto != None):
                    f = tasks.foto
                    with open('static/img/foto_{}.jpg'.format(tasks.nombre), 'wb') as archivo:
                        archivo.write(f)
                        tasks.foto = f 
                session['name']=nombre
            if(request.form['apellido']!=''):
                apellido =request.form['apellido']
                tasks.apellido = apellido
            if(request.form['telf']!=''):
                telefono =request.form['telf']
                tasks.telefono = telefono
            if(request.form['contra']!=''):
                contraseña = request.form['contra']
                password_encode = contraseña.encode("utf-8")
                password_ecriptado = bcrypt.hashpw(password_encode,semilla)
                tasks.contraseña = password_ecriptado
            
            arch = request.files['imagen-usuario']
            #si el usuar
            if(arch.filename!=""):
                print(request.files['imagen-usuario'])
                foto = request.files['imagen-usuario']
                f = foto.read()
                with open('static/img/foto_{}.jpg'.format(tasks.nombre), 'wb') as archivo:
                    archivo.write(f)
                    tasks.foto = f 
            db1.session.commit()
            return render_template('editor-usuario.html', tasks = tasks)
const fs = require('fs')

const cors = require('cors')
const express = require('express')
const ipfsAPI = require('ipfs-api')
const NodeRSA = require('node-rsa');
const path = require("path")
const session = require('express-session')
const axios = require('axios')
var crypto = require('crypto');


require('dotenv').config()

var ipfs = ipfsAPI(process.env.IPFS)

const app = express()

app.use(cors())
var bodyParser = require('body-parser');
app.use(bodyParser.json({limit: '50mb'}));
app.use(bodyParser.urlencoded({limit: '50mb', extended: true}));

var sess = {
  secret: process.env.SECRET,
  cookie: { maxAge: 3600000 },
  proxy: true,
  resave: true,
  saveUninitialized: true
}

if (app.get('env') === 'production') {
  app.set('trust proxy', 1) // trust first proxy
  sess.cookie.secure = true // serve secure cookies
}
app.use(session(sess))


function restrict(req, res, next) {
	console.log(req.session.id)
  if (req.session.user) {
    next();
  } else {
    req.session.error = 'Access denied!';
    res.send(401, 'missing authorization header');
  }
}


const RSA_KEY = new NodeRSA(fs.readFileSync(process.env.RSA_KEY_PATH).toString());

function decodeBase64Image(dataString) {
  var matches = dataString.match(/^data:([A-Za-z-+\/]+);base64,(.+)$/),
    response = {};

  if (matches.length !== 3) {
    return new Error('Invalid input string');
  }

  response.type = matches[1]
  response.extension = matches[1].split("/")[1]
  response.data = Buffer.from(matches[2], 'base64');
  return response;
}

async function generateSignature(folderPath, links){
	let hashes64 = links.map((link) => link.multihash).sort().join(",")
	let dataSign = RSA_KEY.sign(hashes64, 'hex', 'utf8')
	let signature = await storeFile(folderPath, dataSign, "signature.txt")
	return signature;
}

function createHighlight(links){
	let toCreateObject = {
		Data: Buffer.from([0x08, 0x01]),
		Links: links
	}
	
	return new Promise((resolve, reject) => {
		ipfs.object.put(toCreateObject, (err, node) => {
			if(err) reject(err)
			resolve(node)
		})
	})
}

function storeFile(folder, dataContent, filename){
	var filename;
	var content;
	let fileType = filename.split(".").pop()
	if(fileType == "png"){
		var imageBuffer = decodeBase64Image(dataContent);
		content = imageBuffer.data;
		delete imageBuffer;
	}else if(fileType == "json"){
		content = JSON.stringify(dataContent)
	}else if(fileType == "txt"){
		content = dataContent
	}
	var filepath = folder + "/" + filename
	
	return new Promise((resolve, reject) => {
		fs.writeFile(filepath, content, (err) => {
			ipfs.files.add([filepath,], async (e, createdObjects) => {
				createdObjects[0].name = filename
				resolve({
					filepath: filepath,
					ipfsObject: createdObjects[0]
				})
			});
		});
	})
};

const mkdirSync = function (dirPath) {
	console.log(dirPath)
	// FROM: https://stackoverflow.com/a/24311711
	try {
		fs.mkdirSync(dirPath)
	} catch (err) {
		if (err.code !== 'EEXIST') throw err
	}
}

let getHighlightPath = function(highlightId, userHash) {
	let baseFolderPath = path.join(process.env.FILES_PATH, highlightId.substring(0,3))
	let userFolderPath = path.join(baseFolderPath, userHash)
	let folderPath = path.join(userFolderPath, highlightId)
	return [baseFolderPath, userFolderPath, folderPath]
}

let getDataPath = function(referenceId, userHash) {
	let baseFolderPath = path.join(process.env.DATA_PATH, referenceId.substring(0,3))
	let referenceFolderPath = path.join(baseFolderPath, referenceId)
	let ReferenceUserPath = path.join(referenceFolderPath, userHash + ".json")
	return [baseFolderPath, referenceFolderPath, ReferenceUserPath]
}

let mkdirAll = function (folders) {
	for (var i = 0; i < folders.length ; i++) {
		mkdirSync(folders[i])
	}
}

app.post('/highlights', restrict, async (req, res) => {
	let links = []
	let highlightId = req.body.id
	let [baseFolderPath, userFolderPath, folderPath] = getHighlightPath(highlightId, req.session.user.hash)
	mkdirAll([baseFolderPath, userFolderPath, folderPath])
	

	let highlightImage = await storeFile(folderPath, req.body.content.image, "image.png")
	links.push(highlightImage.ipfsObject)
	
	delete req.body.content
	req.body.comment = req.body.comment.text
	req.body.user = req.session.user.hash
	req.body.comment.text
	let infoData = await storeFile(folderPath, req.body, "info.json")
	links.push(infoData.ipfsObject)

	let signature = await generateSignature(folderPath, links)
	links.push(signature.ipfsObject)

	let highlightIpfs = await createHighlight(links)
	res.setHeader('Content-Type', 'application/json')
	let output = highlightIpfs.toJSON()
	delete output.data
	delete output.size
	res.send(JSON.stringify(
		output
	))
})

let readReferenceInfo = function (referenceId, userHash) {
	let [baseFolderPath, referenceFolderPath, datapath] = getDataPath(referenceId, userHash)
	if (fs.existsSync(datapath)) {
		let data = fs.readFileSync(datapath).toString()
		if (data) {
			return JSON.parse(data)
		}
	}
}

app.get('/user_info', (req, res) => {
	if(req.session.user){
		return res.send(JSON.stringify(req.session.user));
	}
	return res.send(401, JSON.stringify({}));
});

app.post('/login', async (req, res) => {
	toSend = {
		email: req.body.user,
		password: req.body.pass
	}
	try{
		let response = await axios.post('https://api.epistemonikos.org/v2.1/accounts/session_tokens', toSend)
		if(response.status == 200){
			return req.session.regenerate(function(){
				req.session.user = {}
				req.session.user.email = toSend.email.toLowerCase()
				req.session.user.token = response.data.session_token
				req.session.user.token_expires_at = response.data.expires_at
				let hash = crypto.createHash('sha256').update(process.env.SECRET + req.session.user.email).digest('base64');
				let hash2 = crypto.createHash('sha256').update(hash).digest('base64');
				req.session.user.hash = hash2
				return res.send(JSON.stringify({'status': 'ok'}))
			});
		}
	}catch(err){
		return req.session.destroy(function(){
		    return res.send(401, JSON.stringify({'status': 'logout'}))
		});
	}
	return req.session.destroy(function(){
	    return res.send(401, JSON.stringify({'status': 'logout'}))
	});
})

app.get('/references/:referenceId', restrict, (req, res) => {
	let referenceId = req.params.referenceId
	let data = readReferenceInfo(referenceId, req.session.user.hash) || {}
	res.setHeader('Content-Type', 'application/json')
	return res.send(JSON.stringify(data))
})

app.post('/references/:referenceId', restrict, (req, res) => {
	let referenceId = req.params.referenceId
	let [baseFolderPath, referenceFolderPath, datapath] = getDataPath(referenceId, req.session.user.hash)
	mkdirAll([baseFolderPath, referenceFolderPath])
	console.log(new Date().toISOString(), "\tREF_ID: ", referenceId, "\t", JSON.stringify(req.body))
	res.setHeader('Content-Type', 'application/json')
	fs.writeFile(datapath, JSON.stringify(req.body), function(err) {
	    if(err) {
	        return res.send(JSON.stringify({'err': err}))
	    }
	    return res.send(JSON.stringify({'status': 'ok'}))
	}); 
})

app.get('/references/:referenceId/highlights', restrict, (req, res) => {
	let referenceId = req.params.referenceId
	let referenceInfo = readReferenceInfo(referenceId, req.session.user.hash) || {}
	let highlights = []
	Object.keys(referenceInfo).forEach(function(key) {
	    let highlightId = referenceInfo[key].highlightId
	    if(highlightId){
			let [baseFolderPath, userFolderPath, highlightPath] = getHighlightPath(highlightId, req.session.user.hash)
			let originalData = fs.readFileSync(path.join(highlightPath, 'image.png'))
			let base64Image = new Buffer(originalData, 'binary').toString('base64')
			let highlightInfo = JSON.parse(fs.readFileSync(path.join(highlightPath, 'info.json')).toString())
			highlightInfo.content = {image: 'data:image/png;base64,' + base64Image}
			highlights.push(highlightInfo)
		}
	});
	res.setHeader('Content-Type', 'application/json')
	return res.send(JSON.stringify(highlights))
})

app.listen(3001, () => console.log('Example app listening on port 3001!'))


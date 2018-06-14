const fs = require('fs')

const cors = require('cors')
const express = require('express')
const ipfsAPI = require('ipfs-api')
const NodeRSA = require('node-rsa');
const path = require("path")

require('dotenv').config()

var ipfs = ipfsAPI(process.env.IPFS)

const app = express()

app.use(cors())
app.use(express.json());

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
				resolve({
					filepath: filepath,
					ipfsObject: createdObjects[0]
				})
			});
		});
	})
};

const mkdirSync = function (dirPath) {
	// FROM: https://stackoverflow.com/a/24311711
	try {
		fs.mkdirSync(dirPath)
	} catch (err) {
		if (err.code !== 'EEXIST') throw err
	}
}

app.post('/', async (req, res) => {
	var links = []

	var highlightID = req.body.id
	var folderPath = path.join(process.env.FILES_PATH, highlightID.substring(0,3))
	mkdirSync(folderPath)
	var folderPath = path.join(folderPath, highlightID)
	mkdirSync(folderPath)

	let highlightImage = await storeFile(folderPath, req.body.content.image, "image.png")
	links.push(highlightImage.ipfsObject)
	
	delete req.body.content
	req.body.comment = req.body.comment.text
	let infoData = await storeFile(folderPath, req.body, "info.json")
	links.push(infoData.ipfsObject)

	let signature = await generateSignature(folderPath, links)
	signature.ipfsObject.name = "signature.txt"
	links.push(signature.ipfsObject)

	let highlightIpfs = await createHighlight(links)
	res.setHeader('Content-Type', 'application/json');
	var output = highlightIpfs.toJSON()
	delete output.data
	delete output.size
	res.send(JSON.stringify(
		output
	))
})

app.listen(3001, () => console.log('Example app listening on port 3001!'))


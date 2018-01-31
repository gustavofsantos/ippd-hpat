const reg = require('all-the-packages');
const fs = require('fs');

reg.on('package', (pkg) => {
	/* writeFileSync é sincrono e não fica dando ruim */
	try {
		//process.stdout.write(`Salvando ${pkg.name.replace(/[+()@/\\*?:\s]/g, '')}...\r`);
		//fs.writeFileSync(`./pacotes/${pkg.name.replace(/[+()@/\\*?:\s]/g, '')}.json`, JSON.stringify(pkg), 'utf8');
        fs.writeFileSync(`./pacotes/${pkg.name}.json`, JSON.stringify(pkg), 'utf8');
        process.stdout.write(`Salvando ${pkg.name}...\r`);
	}
	catch (err) {
		process.stdout.write('Erro.\r');
	}
});

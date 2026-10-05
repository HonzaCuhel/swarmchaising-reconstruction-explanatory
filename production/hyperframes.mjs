// Resolve the pinned CLI from project dependencies or an existing local cache.
// Does not modify permissions, browser flags, global configuration or credentials.
import fs from 'node:fs';
import path from 'node:path';
import os from 'node:os';
import {fileURLToPath} from 'node:url';
import {spawnSync} from 'node:child_process';
const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const pinned=JSON.parse(fs.readFileSync(path.join(root,'package.json'),'utf8')).devDependencies.hyperframes;
const candidates=[];
if(process.env.HYPERFRAMES_CLI)candidates.push(process.env.HYPERFRAMES_CLI);
candidates.push(path.join(root,'node_modules/hyperframes/dist/cli.js'));
const cacheRoots=[process.env.npm_config_cache,path.join(os.homedir(),'.npm'),path.join(os.homedir(),'.npm-hf-cache')].filter(Boolean);
for(const cache of cacheRoots){
 const npx=path.join(cache,'_npx');
 if(fs.existsSync(npx))for(const dir of fs.readdirSync(npx))candidates.push(path.join(npx,dir,'node_modules/hyperframes/dist/cli.js'));
}
const cli=candidates.find(candidate=>{
 try{return fs.existsSync(candidate)&&JSON.parse(fs.readFileSync(path.resolve(candidate,'../../package.json'),'utf8')).version===pinned;}catch{return false;}
});
if(!cli){console.error(`HyperFrames ${pinned} is not installed. Run npm install in the repository, then retry. No renderer substitution was attempted.`);process.exit(2);}
const result=spawnSync(process.execPath,[cli,...process.argv.slice(2)],{cwd:root,stdio:'inherit',env:{...process.env,HYPERFRAMES_NO_TELEMETRY:'1'}});
if(result.error){console.error(result.error.message);process.exit(1);}
process.exit(result.status??1);

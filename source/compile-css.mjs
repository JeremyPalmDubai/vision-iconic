import fs from 'node:fs/promises';
import {compile} from 'tailwindcss';
let css=await fs.readFile('styles.css','utf8');
css=css.replace('@import "tailwindcss";', await fs.readFile('node_modules/tailwindcss/theme.css','utf8')+'\n'+await fs.readFile('node_modules/tailwindcss/preflight.css','utf8')+'\n@tailwind utilities;');
const output=await compile(css);
await fs.writeFile('dist/assets/style.css',output.build(['flex','grid','relative','absolute','items-center','justify-between','w-full','h-full','text-white','bg-black']));
console.log('Tailwind CSS compiled');

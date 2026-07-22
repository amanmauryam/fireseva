const esbuild = require("esbuild");
const fs = require("fs");
const path = require("path");

const inputDir = path.join(__dirname, "../static/js");
const outputDir = path.join(inputDir, "dist");

// dist folder create if not exists
if (!fs.existsSync(outputDir)) {
    fs.mkdirSync(outputDir, { recursive: true });
}

// Read all js files
const files = fs.readdirSync(inputDir);

files.forEach(async (file) => {
    if (
        file.endsWith(".js") &&
        !file.endsWith(".min.js") &&
        file !== "build.js"
    ) {
        const inputFile = path.join(inputDir, file);

        const outputFile = path.join(
            outputDir,
            file.replace(".js", ".min.js")
        );

        try {
            await esbuild.build({
                entryPoints: [inputFile],
                outfile: outputFile,
                bundle: false,
                minify: true,
                sourcemap: false,
                target: ["es2018"],
            });

            console.log(`✅ ${file} → dist/${path.basename(outputFile)}`);
        } catch (err) {
            console.error(`❌ Error in ${file}`);
            console.error(err.message);
        }
    }
});
// meme-rogue-v3: copy the rendered entry image into /output/entry.png.
// The gate reads /output/entry.png: a whole PNG, at most 1 MiB, at most 1024x1024.
import { copyFileSync, readFileSync, mkdirSync, chmodSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const dir = dirname(fileURLToPath(import.meta.url));
const src = join(dir, "entry.png");
const buf = readFileSync(src);
const PNG_MAGIC = [0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a];
if (buf.length < 8 || !PNG_MAGIC.every((b, i) => buf[i] === b)) {
  throw new Error("entry.png is not a whole PNG");
}
if (buf.length > 1048576) {
  throw new Error("entry.png exceeds 1 MiB");
}
mkdirSync("/output", { recursive: true });
const target = "/output/entry.png";
copyFileSync(src, target);
chmodSync(target, 0o644);
// The PNG bytes are copied verbatim: no re-encode, no resize, no metadata edits,
// so the two grader runs see byte-identical output.

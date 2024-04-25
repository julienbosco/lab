import * as fs from "fs";
import { Document, Paragraph, TextRun, Packer, ImageRun, convertMillimetersToTwip} from "docx";

const doc = new Document({
  sections: [
    {
      properties: {},
      children: [
        new Paragraph({
          alignment: 'center',
          children: [
            new ImageRun({
              data: fs.readFileSync("./assets/logo-cegep-page-titre.png"),
              transformation: {
                width: convertMillimetersToTwip(9.7),
                height: convertMillimetersToTwip(2.9),
              },
            }),
          ],
        }),
        new Paragraph({
          children: [
            new TextRun("Salut le monde!")
          ],
        }),
      ],
    },
  ],
});

Packer.toBuffer(doc).then((buffer) => {
fs.writeFileSync("mydoc.docx", buffer);
});



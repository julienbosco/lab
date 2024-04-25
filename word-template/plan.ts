import * as fs from 'fs';
import { Document, Packer, Paragraph, TextRun, HeadingLevel, AlignmentType } from 'docx';

// Fonction pour créer une section avec un titre et un paragraphe vide
function createSection(document: Document, sections: Record<string, Paragraph>) {
    for (const sectionTitle in sections) {
        if (sections.hasOwnProperty(sectionTitle)) {
            const heading = new Paragraph({
                children: [new TextRun(sectionTitle)],
                heading: HeadingLevel.HEADING_1,
                thematicBreak: true,
            });
            document.addChildElement(heading); // Ajout du paragraphe au document
            const emptyParagraph = new Paragraph("");
            document.addChildElement(emptyParagraph); // Ajout du paragraphe vide au document
            sections[sectionTitle] = emptyParagraph; // Mise à jour du dictionnaire avec le paragraphe vide
        }
    }
}

// Création du document
const document = new Document();

// Page titre
const titlePage = new Paragraph({
    children: [
        new TextRun("PLAN DE COURS"),
    ],
    alignment: AlignmentType.CENTER,
});
document.addChildElement(titlePage);

// Dictionnaire contenant les sections avec des paragraphes vides
const sections: Record<string, Paragraph> = {
    "Notes préliminaires": new Paragraph(""),
    "Compétences transversales": new Paragraph(""),
    "Objectif et standard": new Paragraph(""),
    "Contenus du cours, activités d’enseignement et d’apprentissage et échéancier": new Paragraph(""),
    "Plan d’évaluation": new Paragraph(""),
    "Modalités d’évaluation des compétences langagières": new Paragraph(""),
    "Modalités d’encadrement": new Paragraph(""),
    "Modalités de communication et de prise de rendez-vous": new Paragraph(""),
    "Matériel didactique obligatoire et facultatif, médiagraphie": new Paragraph(""),
    "Modes de rétroaction sur le déroulement du cours": new Paragraph(""),
    "Politiques institutionnelles et règles départementales pertinente pour le cours": new Paragraph(""),
};

// Ajout des sections au document et mise à jour du dictionnaire
createSection(document, sections);

// Remplissage des sections
sections["Notes préliminaires"].addRun(new TextRun("Contenu des notes préliminaires..."));
sections["Compétences transversales"].addRun(new TextRun("Contenu des compétences transversales..."));
// Ajoutez le contenu pour chaque section comme cela...

// Génération du fichier docx
Packer.toBuffer(document).then(buffer => {
    fs.writeFileSync("plan_de_cours.docx", buffer);
    console.log("Gabarit de plan de cours généré avec succès !");
}).catch(err => {
    console.log("Une erreur est survenue :", err);
});


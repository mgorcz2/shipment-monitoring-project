import pl from "./pl";


const userLang = navigator.language || navigator.userLanguage; 
const lang = userLang.startsWith("pl") ? "pl" : "en"; 

export const translate = (msg, lang) => {
  if (lang === "pl" && pl[msg]) return pl[msg];
  return msg;
};
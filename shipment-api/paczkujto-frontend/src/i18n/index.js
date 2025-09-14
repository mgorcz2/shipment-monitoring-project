import pl from "./pl";


const userLang = navigator.language || navigator.userLanguage; 
const user_lang = userLang.startsWith("pl") ? "pl" : "en"; 

export const translate = (msg, lang=user_lang) => {
  if (lang === "pl" && pl[msg]) return pl[msg];
  return msg;
};
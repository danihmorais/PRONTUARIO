import { getVersion } from "@tauri-apps/api/app";
import { invoke } from "@tauri-apps/api/tauri";

const REPO_URL = "https://api.github.com/repos/danihmorais/PRONTUARIO/releases/latest";

export async function verificarAtualizacao() {
  try {
    const res = await fetch(REPO_URL);
    if (!res.ok) return;
    
    const data = await res.json();
    const latestTag = data.tag_name; 
    const currentVersion = await getVersion();
    
    const cleanTag = latestTag.replace("v", "");
    
    if (cleanTag !== currentVersion) {
      const asset = data.assets.find((a: any) => a.name.toLowerCase().endsWith(".exe"));
      
      if (asset) {
        const dataPub = new Date(data.published_at).toLocaleDateString("pt-BR");
        const confirmar = window.confirm(
          `Nova versão disponível: ${latestTag}\nPublicada em: ${dataPub}\n\nDeseja baixar e atualizar agora?`
        );
        
        if (confirmar) {
          alert("O sistema está a descarregar a atualização em segundo plano.\n\nA aplicação será reiniciada automaticamente ao concluir. Por favor, aguarde e não feche o sistema.");
          await invoke("aplicar_atualizacao", { url: asset.browser_download_url });
        }
      }
    }
  } catch (error) {
    console.error("Erro ao verificar atualização:", error);
  }
}
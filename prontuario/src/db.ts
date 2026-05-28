import { invoke } from "@tauri-apps/api/tauri";

export async function dbExecute(sql: string, params: string[] = []): Promise<number> {
  return await invoke("db_execute", { sql, params });
}

export async function dbQuery<T = any>(sql: string, params: string[] = []): Promise<T[]> {
  return await invoke("db_query", { sql, params });
}
# TonerDesk

Acesso remoto da Tonertech para atendimentos, baseado no [RustDesk](https://github.com/rustdesk/rustdesk)
(licença AGPL-3.0 — este repositório público com o código modificado cumpre a licença).

## O que foi alterado em relação ao RustDesk

| Item | Onde |
|---|---|
| Nome do programa `TonerDesk` (janela, instalação em `C:\Program Files\TonerDesk`, serviço, pasta de config `%AppData%\TonerDesk`) | `libs/hbb_common/src/config.rs` (`APP_NAME`) |
| Servidor e chave definidos na compilação (secrets `RENDEZVOUS_SERVER` e `RS_PUB_KEY`) | `libs/hbb_common/src/config.rs` |
| Ícones e logo | `branding/gerar_marca.py` (gera tudo; troque as cores ou coloque `branding/icone_custom.png`) |
| Nome/descrição do .exe | `Cargo.toml`, `libs/portable/Cargo.toml`, `flutter/windows/runner/Runner.rc` |
| Build só Windows x64, gera `TonerDesk.exe` em uma Release | `.github/workflows/tonerdesk-windows.yml` |

Por ser um "cliente personalizado", o TonerDesk **não** se auto-atualiza para o RustDesk oficial.
`libs/hbb_common` deixou de ser submódulo e passou a fazer parte do repositório.

## Gerar uma nova versão

1. GitHub → aba **Actions** → **TonerDesk - Build Windows** → **Run workflow** → informe a versão (ex.: `v1.0.1`).
2. Leva ~40–60 min na primeira vez (depois fica mais rápido com cache).
3. O arquivo sai em **Releases** → `TonerDesk.exe`.

## Uso no atendimento (igual AnyDesk)

- **Cliente:** baixa e abre o `TonerDesk.exe` (não precisa instalar). Passa o **ID** e a **senha** que aparecem na tela.
- **Técnico:** abre o TonerDesk, digita o ID do cliente, conecta e informa a senha (ou o cliente clica em *Aceitar*).
- Para máquinas com contrato/atendimento recorrente: no cliente, botão **Instalar** → definir **senha permanente**
  em Configurações → Segurança. Assim dá para acessar sem ninguém na frente do PC.

## Servidor próprio gratuito (recomendado)

Sem servidor próprio, o TonerDesk usa o servidor público do RustDesk (funciona, mas pode ficar lento em horários de pico).
Para ter servidor próprio sem custo:

**Opção A – Oracle Cloud "Always Free"** (VM grátis permanente, Ubuntu):
1. Crie a conta em cloud.oracle.com e uma VM Ubuntu (shape *Ampere A1* ou *E2.1.Micro*, ambas no Always Free).
2. Libere as portas na *Security List* da VCN e no firewall da VM: **TCP 21115–21119** e **UDP 21116**.
3. Na VM:
   ```bash
   sudo apt update && sudo apt install -y docker.io docker-compose-v2
   mkdir -p ~/tonerdesk-server && cd ~/tonerdesk-server
   # salve o docker-compose.yml desta pasta (server/docker-compose.yml) aqui
   sudo docker compose up -d
   cat data/id_ed25519.pub     # esta é a CHAVE (RS_PUB_KEY)
   ```

**Opção B – um PC/servidor da empresa ligado 24h** com IP fixo ou DDNS (No-IP/DuckDNS grátis):
mesmo `docker-compose.yml` (ou os executáveis `hbbs`/`hbbr` para Windows) e redirecionar no roteador as portas acima.

### Depois que o servidor estiver no ar

No GitHub: **Settings → Secrets and variables → Actions → New repository secret**
- `RENDEZVOUS_SERVER` = IP público ou domínio do servidor
- `RS_PUB_KEY` = conteúdo de `id_ed25519.pub`

Rode o workflow de novo: o novo `TonerDesk.exe` já sai apontando para o servidor de vocês.
(Enquanto isso, dá para testar manualmente em TonerDesk → Configurações → Rede → Servidor ID/Relay.)

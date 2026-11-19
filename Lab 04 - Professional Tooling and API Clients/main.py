
def main() -> None:
    """Demostración principal del proyecto Lab 04."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
    )

    print("==================================================================")
    print("   LAB 04: LOG PIPELINE REVAMP & PROFESSIONAL TOOLING VERIFIED   ")
    print("==================================================================")

    # Crear archivo de log temporal de prueba
    test_log = Path("/workspace/scratch/sample_lab04.log")
    test_log.write_text(
        "2026-11-19 14:00:00 [INFO] auth_service: User login successful\n"
        "2026-11-19 14:01:20 [ERROR] db_service: Connection timeout to postgres\n"
        "LINEA CORRUPTA SIN FORMATO VALIDO\n"
        "2026-11-19 14:02:45 [ERROR] payment_gateway: Card processor declined transaction\n"
        "2026-11-19 14:05:10 [WARNING] auth_service: High latency detected\n",
        encoding="utf-8"
    )

    print("\n[+] Procesando archivo de logs con log_pipeline_revamp:")
    total_errors = run_cli_pipeline(test_log)

    print(f"\n[+] Total de errores procesados con streaming perezoso: {total_errors}")
    print("==================================================================")


if __name__ == "__main__":
    main()

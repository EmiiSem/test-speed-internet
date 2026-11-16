#!/usr/bin/env python3
"""Десять последовательных загрузок URL и скорость скачивания."""

import argparse
import sys
import time
import urllib.error
import urllib.request

REQUEST_COUNT = 10
USER_AGENT = "test-speed-internet/1.0"
# Десятичные единицы СИ: 1 МБ = 10^6 байт, 1 Мбит/с = 10^6 бит/с.
MEGA = 1_000_000


def download(url: str, timeout: float) -> tuple[int, float]:
    """Скачивает ответ целиком и возвращает размер тела и длительность."""
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    started = time.perf_counter()
    with urllib.request.urlopen(request, timeout=timeout) as response:
        body = response.read()
    elapsed = time.perf_counter() - started
    return len(body), elapsed


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Делает 10 последовательных запросов к адресу, "
            "считает среднее время, объём и скорость скачивания."
        )
    )
    parser.add_argument("url", help="Адрес ресурса, например URL тяжёлой картинки")
    parser.add_argument(
        "--timeout",
        type=float,
        default=60,
        metavar="SECONDS",
        help="Таймаут одного запроса в секундах (по умолчанию 60)",
    )
    args = parser.parse_args()

    total_bytes = 0
    total_seconds = 0.0

    for index in range(1, REQUEST_COUNT + 1):
        try:
            size, elapsed = download(args.url, args.timeout)
        except (urllib.error.URLError, TimeoutError, OSError) as error:
            print(
                f"Запрос {index}/{REQUEST_COUNT} не удался: {error}",
                file=sys.stderr,
            )
            return 1

        total_bytes += size
        total_seconds += elapsed
        print(f"{index:2}/{REQUEST_COUNT}  {elapsed:.3f} с  {size} байт")

    average_seconds = total_seconds / REQUEST_COUNT
    total_megabytes = total_bytes / MEGA
    speed_mbps = (total_bytes * 8) / total_seconds / MEGA

    print()
    print(f"Среднее время запроса: {average_seconds:.3f} с")
    print(f"Общий объём: {total_bytes} байт ({total_megabytes:.3f} МБ)")
    print(f"Скорость скачивания: {speed_mbps:.2f} Мбит/с")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

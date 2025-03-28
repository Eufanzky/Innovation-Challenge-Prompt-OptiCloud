import httpx # Be sure to add 'httpx' to 'requirements.txt'
import asyncio

async def stream_generator(file_path):
    chunk_size = 2 * 1024  # Define your own chunk size
    with open(file_path, 'rb') as file:
        while chunk := file.read(chunk_size):
            yield chunk
            print(f"Sent chunk: {len(chunk)} bytes")

async def stream_to_server(url, file_path):
    timeout = httpx.Timeout(60.0, connect=60.0)
    async with httpx.AsyncClient(timeout=timeout) as client:
        response = await client.post(url, content=stream_generator(file_path))
        return response

async def stream_response(response):
    if response.status_code == 200:
        async for chunk in response.aiter_raw():
            print(f"Received chunk: {len(chunk)} bytes")
    else:
        print(f"Error: {response}")

async def main():
    print('helloworld')
    # Customize your streaming endpoint served from core tool in variable 'url' if different.
    url = 'http://localhost:7071/streaming_upload'
    file_path = r'E:\INFORMATICA\Innovation-Challenge-Prompt-OptiCloud\azure-function\fast_api\static\reviews\review1.txt'

    response = await stream_to_server(url, file_path)
    print(response)

if __name__ == "__main__":
    asyncio.run(main())
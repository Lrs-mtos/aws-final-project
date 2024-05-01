import json
import boto3
import os

BUCKET_NAME = 'bucket-salva-matricula-final-project'
SNS_TOPIC_ARN = 'arn:aws:sns:us-east-1:117793179715:final-project-sns-topic'

s3 = boto3.client('s3')
sns = boto3.client('sns')

def lambda_handler(event, context):
    try:
        # Verifica se o corpo da solicitação está presente e é um JSON válido
        if 'body' in event:
            body = json.loads(event['body'])
            matricula = body['matricula']
            email = body['email']
            
            # Cria um nome de arquivo baseado na matrícula
            file_name = f"matricula-{matricula}"
            
            # Faz o upload do conteúdo para o S3
            s3.put_object(
                Bucket=BUCKET_NAME,
                Key=file_name,
                Body=matricula
            )
            
            # Gerar URL pré-assinada para upload de arquivo
            presigned_url = s3.generate_presigned_url(
                ClientMethod='put_object',
                Params={
                    'Bucket': BUCKET_NAME,
                    'Key': file_name,
                    'ContentType': 'application/pdf'  # Defina o tipo de conteúdo do arquivo aqui
                }
            )
            
            # Envie uma mensagem SNS para o endereço de e-mail fornecido
            sns.publish(
                TopicArn=SNS_TOPIC_ARN,
                Message=f'O upload do arquivo para a matrícula {matricula} foi bem-sucedido. O link pré-assinado para o arquivo é: {presigned_url}',
                Subject='Upload de Arquivo Bem-Sucedido'
            )
            
            return {
                'statusCode': 200,
                'body': json.dumps({
                    'message': 'Matrícula e URL pré-assinada gerada com sucesso. Um e-mail de confirmação foi enviado.',
                    'preSignedUrl': presigned_url
                })
            }
        else:
            return {
                'statusCode': 400,
                'body': json.dumps('Nenhum corpo de solicitação fornecido.')
            }

    except json.JSONDecodeError:
        return {
            'statusCode': 400,
            'body': json.dumps('Entrada JSON inválida.')
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps(f'Erro ao processar a solicitação: {str(e)}')
        }
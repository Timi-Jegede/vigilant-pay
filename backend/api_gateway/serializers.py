from rest_framework import serializers

class SenderSerializer(serializers.Serializer):
    external_id = serializers.IntegerField()
    device_fingerprint = serializers.CharField(max_length=256) 

class RecipientSerializer(serializers.Serializer):
    account_number_hash = serializers.CharField(max_length=64)

class InnerTransactionSerializers(serializers.Serializer):
    transaction_id = serializers.UUIDField(format='hex_verbose')
    amount = serializers.DecimalField(max_digits=12, decimal_places=2)
    current_available_balance = serializers.DecimalField(max_digits=12, decimal_places=2)
 

class TransactionSerializer(serializers.Serializer):
    sender = SenderSerializer()
    recipient = RecipientSerializer()
    transaction = InnerTransactionSerializers()

    def validate(self, payload):
        transaction_data = payload.get('transaction', {})
        amount = transaction_data.get('amount')
        current_available_balance = transaction_data.get('current_available_balance')

        errors = {}

        if amount is not None and amount <= 0:
                errors['amount'] = 'Transaction amount must be greater that zero.'
        
        if current_available_balance is not None and current_available_balance <= 0:
                errors['current_available_balance'] = 'Available balance must be greater than zero.'
        
        if errors:
                raise serializers.ValidationError({'transaction': errors})
        
        return payload

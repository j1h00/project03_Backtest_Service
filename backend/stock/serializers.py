from rest_framework import serializers

from accounts.serializers import UserSerializer
from .models import FinancialKonex, FinancialKosdaq, FinancialKospi, InfoKonex, InfoKosdaq, InfoKospi, BoardKospi

# ====================================================================== 코스피 ======================================================================
class InfoKospiSerializer(serializers.ModelSerializer):
    class Meta:
        model = InfoKospi
        fields = '__all__'
        
class FinancialKospiSerializer(serializers.ModelSerializer):
    info_kospi = InfoKospiSerializer(read_only=True)
    
    class Meta:
        model = FinancialKospi
        fields = '__all__'
        
class BoardKospiSerializer(serializers.ModelSerializer):
    info_kospi = InfoKospiSerializer(read_only=True)
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = BoardKospi
        fields = '__all__'
        
# ====================================================================== 코스닥 ======================================================================
class InfoKosdaqSerializer(serializers.ModelSerializer):
    class Meta:
        model = InfoKosdaq
        fields = '__all__'
        
class FinancialKosdaqSerializer(serializers.ModelSerializer):
    info_kosdaq = InfoKosdaqSerializer(read_only=True)
    
    class Meta:
        model = FinancialKosdaq
        fields = '__all__'
        
# ====================================================================== 코넥스 ======================================================================
class InfoKonexSerializer(serializers.ModelSerializer):
    class Meta:
        model = InfoKonex
        fields = '__all__'
        
class FinancialKonexSerializer(serializers.ModelSerializer):
    info_konex = InfoKonexSerializer(read_only=True)
    
    class Meta:
        model = FinancialKonex
        fields = '__all__'
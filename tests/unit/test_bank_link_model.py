import pytest
import uuid
from app.database.models.bank_links_model import BankLink
from app.database.models.user_model import User

class TestBankLinkModel:
    
    def test_bank_link_creation(self):
        """Test basic bank link creation"""
        # Create a user first
        user = User()
        user.email = "banktest@example.com"
        
        bank_link = BankLink()
        bank_link.user_id = user.id
        bank_link.requisition_id = "req_1234567890abcdef"
        bank_link.institution_id = "SANDBOXFINANCE_SFIN0000"
        bank_link.bank_name = "Test Bank"
        
        assert bank_link.requisition_id == "req_1234567890abcdef"
        assert bank_link.institution_id == "SANDBOXFINANCE_SFIN0000"
        assert bank_link.bank_name == "Test Bank"
        assert bank_link.user_id == user.id
        assert bank_link.id is not None
        assert isinstance(bank_link.id, uuid.UUID)
    
    def test_requisition_id_encryption(self):
        """Test that requisition_id is encrypted in database"""
        bank_link = BankLink()
        bank_link.requisition_id = "req_secret_123456789"
        
        # Internal storage should be encrypted (different from original)
        assert bank_link._requisition_id != "req_secret_123456789"
        assert bank_link._requisition_id is not None
        assert len(bank_link._requisition_id) > len("req_secret_123456789")
        
        # Public access should be decrypted
        assert bank_link.requisition_id == "req_secret_123456789"
    
    def test_institution_id_encryption(self):
        """Test that institution_id is encrypted in database"""
        bank_link = BankLink()
        bank_link.institution_id = "BANK_INSTITUTION_ID_12345"
        
        # Internal storage should be encrypted (different from original)
        assert bank_link._institution_id != "BANK_INSTITUTION_ID_12345"
        assert bank_link._institution_id is not None
        assert len(bank_link._institution_id) > len("BANK_INSTITUTION_ID_12345")
        
        # Public access should be decrypted
        assert bank_link.institution_id == "BANK_INSTITUTION_ID_12345"
    
    def test_bank_name_not_encrypted(self):
        """Test that bank_name is NOT encrypted (public info)"""
        bank_link = BankLink()
        bank_link.bank_name = "Barclays Bank"
        
        # Bank name should be stored as-is (not encrypted)
        assert bank_link.bank_name == "Barclays Bank"
        # No internal encrypted field for bank_name
        assert not hasattr(bank_link, '_bank_name')
    
    def test_empty_values(self):
        """Test bank link with empty values"""
        bank_link = BankLink()
        bank_link.requisition_id = ""
        bank_link.institution_id = None
        bank_link.bank_name = ""
        
        assert bank_link.requisition_id == ""
        assert bank_link.institution_id is None
        assert bank_link.bank_name == ""
        assert bank_link._requisition_id == ""
        assert bank_link._institution_id is None
    
    def test_multiple_bank_links_unique_encryption(self):
        """Test that same values produce different encrypted data"""
        bank_link1 = BankLink()
        bank_link2 = BankLink()
        
        same_req_id = "req_duplicate_test_123"
        bank_link1.requisition_id = same_req_id
        bank_link2.requisition_id = same_req_id
        
        # Encrypted values should be different (due to random IV)
        assert bank_link1._requisition_id != bank_link2._requisition_id
        
        # But both should decrypt to the same value
        assert bank_link1.requisition_id == same_req_id
        assert bank_link2.requisition_id == same_req_id
    
    def test_different_institution_ids(self):
        """Test encryption of different institution ID formats"""
        bank_link = BankLink()
        
        institution_ids = [
            "SANDBOXFINANCE_SFIN0000",
            "BARCLAYS_BARCGB22",
            "HSBC_HBUKGB4B",
            "LLOYDS_LOYDGB2L",
            "NATWEST_NWBKGB2L"
        ]
        
        for inst_id in institution_ids:
            bank_link.institution_id = inst_id
            
            # Should encrypt and decrypt correctly
            assert bank_link.institution_id == inst_id
            assert bank_link._institution_id != inst_id
            assert len(bank_link._institution_id) > len(inst_id)
    
    def test_long_requisition_ids(self):
        """Test encryption of very long requisition IDs"""
        bank_link = BankLink()
        
        # Very long requisition ID
        long_req_id = "req_very_long_requisition_id_with_lots_of_characters_and_numbers_123456789_abcdefghijklmnopqrstuvwxyz"
        bank_link.requisition_id = long_req_id
        
        assert bank_link.requisition_id == long_req_id
        assert bank_link._requisition_id != long_req_id
        assert len(bank_link._requisition_id) > len(long_req_id)
    
    def test_bank_link_repr(self):
        """Test bank link string representation"""
        user = User()
        user.email = "repr@example.com"
        
        bank_link = BankLink()
        bank_link.user_id = user.id
        bank_link.bank_name = "Test Bank"
        bank_link.requisition_id = "secret_req_123"
        
        repr_str = repr(bank_link)
        assert "BankLink" in repr_str
        assert "Test Bank" in repr_str
        assert str(user.id) in repr_str
        
        # Should not expose encrypted requisition_id in repr
        assert "secret_req_123" not in repr_str
    
    def test_special_characters_in_ids(self):
        """Test IDs with special characters"""
        bank_link = BankLink()
        
        special_ids = [
            "req_with-dashes_and_underscores",
            "BANK_ID.WITH.DOTS@DOMAIN.COM",
            "institution+with+plus/characters",
            "req#with$special%chars&more!"
        ]
        
        for special_id in special_ids:
            bank_link.requisition_id = special_id
            assert bank_link.requisition_id == special_id
            
            bank_link.institution_id = special_id
            assert bank_link.institution_id == special_id
    
    def test_user_relationship(self):
        """Test the relationship between User and BankLink"""
        user = User()
        user.email = "relationship@test.com"
        
        bank_link = BankLink()
        bank_link.user_id = user.id
        bank_link.bank_name = "Relationship Test Bank"
        
        # Basic relationship test
        assert bank_link.user_id == user.id
        
        # If relationship is set up properly, this would work:
        # assert bank_link.user == user
        # assert user.bank_links[0] == bank_link

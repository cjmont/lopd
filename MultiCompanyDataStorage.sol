// MultiCompanyDataStorage.sol
pragma solidity ^0.8.0;

contract MultiCompanyDataStorage {
    struct Data {
        string encryptedData;
        string detalle;
        bool exists;
    }

    struct Company {
        bool exists;
        mapping(string => Data) data;
    }

    mapping(address => mapping(string => Company)) private companies;

    event CompanyCreated(address indexed owner, string companyId);
    event DataAdded(address indexed owner, string companyId, string dataId, string encryptedData, string detalle);

    function createCompany(string memory companyId) public {
        require(!companies[msg.sender][companyId].exists, "Company already exists");
        companies[msg.sender][companyId].exists = true;
        emit CompanyCreated(msg.sender, companyId);
    }

    function addData(string memory companyId, string memory dataId, string memory _encryptedData, string memory _detalle) public {
        require(companies[msg.sender][companyId].exists, "Company does not exist");
        companies[msg.sender][companyId].data[dataId] = Data(_encryptedData, _detalle, true);
        emit DataAdded(msg.sender, companyId, dataId, _encryptedData, _detalle);
    }

    function getData(string memory companyId, string memory dataId) public view returns (string memory, string memory) {
        require(companies[msg.sender][companyId].exists, "Company does not exist");
        require(companies[msg.sender][companyId].data[dataId].exists, "Data does not exist");
        Data memory data = companies[msg.sender][companyId].data[dataId];
        return (data.encryptedData, data.detalle);
    }
}

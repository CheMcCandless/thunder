import shutil
import tempfile
from numpy import array, array_equal
from thunder.clustering.kmeans import kmeans
from test_utils import PySparkTestCase


class ClusteringTestCase(PySparkTestCase):
    def setUp(self):
        super(ClusteringTestCase, self).setUp()
        self.outputdir = tempfile.mkdtemp()

    def tearDown(self):
        super(ClusteringTestCase, self).tearDown()
        shutil.rmtree(self.outputdir)


class TestKMeans(ClusteringTestCase):
    def test_kmeans(self):
        """ With k=1 always get one cluster centered on the mean"""

        data_local = [
            array([1.0, 2.0, 6.0]),
            array([1.0, 3.0, 0.0]),
            array([1.0, 4.0, 6.0])]

        data = self.sc.parallelize(zip(range(1, 4), data_local))

        labels, centers = kmeans(data, k=1, maxiter=20, tol=0.001)
        assert array_equal(centers[0], array([1.0, 3.0, 4.0]))
        assert array_equal(labels.map(lambda (_, v): v).collect(), array([0, 0, 0]))



